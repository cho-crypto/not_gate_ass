from pathlib import Path
import json, xml.etree.ElementTree as E
R=Path(__file__).resolve().parent
for d in ['vhdl','testbench','logisim','tests','results','synthesis','figures','output/pdf','tmp']: (R/d).mkdir(parents=True,exist_ok=True)
class Circuit:
 def __init__(self,name,inputs): self.name=name;self.inputs=inputs;self.gates=[];self.outputs=['q','qb'];self.labels={}
 def gate(self,kind,out,*args): self.gates.append((kind,out,list(args)));return out
 def nand(self,out,a,b): return self.gate('NAND',out,a,b)
 def inv(self,out,a): return self.nand(out,a,a)
 def latch(self,p,d,en,q,qb):
  dn=self.inv(p+'dn',d);sb=self.nand(p+'sb',d,en);rb=self.nand(p+'rb',dn,en)
  self.nand(q,sb,qb);self.nand(qb,rb,q)
 def nand3(self,p,out,a,b,c):
  n=self.nand(p+'n',a,b);ab=self.inv(p+'ab',n);return self.nand(out,ab,c)
 def alatch(self,p,d,en,q,qb):
  dn=self.inv(p+'dn',d);sb=self.nand(p+'sb',d,en);rb=self.nand(p+'rb',dn,en)
  self.nand3(p+'qs',q,sb,qb,'setn');self.nand3(p+'qr',qb,rb,q,'clrn')
cs=[]
c=Circuit('rs_latch',['s','r']);c.gate('NOR','q','r','qb');c.gate('NOR','qb','s','q');cs.append(c)
c=Circuit('d_latch',['d','en']);c.latch('', 'd','en','q','qb');cs.append(c)
c=Circuit('d_ff',['d','clk']);c.gate('NOT','clkn','clk');c.latch('m_', 'd','clkn','mq','mqb');c.latch('s_', 'mq','clk','q','qb');cs.append(c)
c=Circuit('jk_ff',['j','k','clk']);c.inv('clkn','clk');c.inv('kn','k');c.nand('jterm','j','qb');c.nand('kterm','kn','q');c.nand('next_d','jterm','kterm');c.latch('m_','next_d','clkn','mq','mqb');c.latch('s_','mq','clk','q','qb');cs.append(c)
c=Circuit('d_ff_async',['d','clk','set','clr']);c.inv('clkn','clk');c.inv('clrn','clr');c.nand('setn','set','clrn');c.nand('busy_n','clr','clr');c.nand('idle_n','clrn','setn');c.inv('idle','idle_n');c.nand('men_n','clkn','idle');c.inv('men','men_n');c.nand('sen_n','clk','idle');c.inv('sen','sen_n');c.alatch('m_','d','men','mq','mqb');c.alatch('s_','mq','sen','q','qb');cs.append(c)
# Remove unused node.
cs[-1].gates=[g for g in cs[-1].gates if g[1]!='busy_n']
header='library ieee;\nuse ieee.std_logic_1164.all;\n\n'
rtl={
'rs_latch':'''  -- Active-high NOR latch. s=r=1 forces q=qb=0 (forbidden).
  -- Releasing both controls simultaneously is not a valid state recovery.
  q_i <= not (r or qb_i);
  qb_i <= not (s or q_i);
  q <= q_i; qb <= qb_i;''',
'd_latch':'''  process(d, en)
  begin
    if en = '1' then q_i <= d; end if;
  end process;
  q <= q_i; qb <= not q_i;''',
'd_ff':'''  process(clk)
  begin
    if rising_edge(clk) then q_i <= d; end if;
  end process;
  q <= q_i; qb <= not q_i;''',
'jk_ff':'''  process(clk)
  begin
    if rising_edge(clk) then
      if j = '0' and k = '1' then q_i <= '0';
      elsif j = '1' and k = '0' then q_i <= '1';
      elsif j = '1' and k = '1' then q_i <= not q_i;
      end if;
    end if;
  end process;
  q <= q_i; qb <= not q_i;''',
'd_ff_async':'''  process(clk, set, clr)
  begin
    if clr = '1' then q_i <= '0';
    elsif set = '1' then q_i <= '1';
    elsif rising_edge(clk) then q_i <= d;
    end if;
  end process;
  q <= q_i; qb <= not q_i;'''}
for c in cs:
 ports='; '.join(f'{i} : in std_logic' for i in c.inputs)+'; q, qb : out std_logic'
 ent=f'entity {c.name} is\n  port (\n'+''.join(f'    {i} : in std_logic;\n' for i in c.inputs)+'    q, qb : out std_logic\n  );\nend entity;\n\n'
 sig='signal q_i, qb_i : std_logic;' if c.name=='rs_latch' else 'signal q_i : std_logic;'
 (R/'vhdl'/f'{c.name}.vhd').write_text(header+ent+f'architecture rtl of {c.name} is\n  {sig}\nbegin\n'+rtl[c.name]+'\nend architecture;\n')
 # Gate netlist with finite gate propagation delay, used for independent equivalence simulation.
 signals=[g[1] for g in c.gates if g[1] not in c.outputs]
 ge=f'entity {c.name}_gates is\n  port ({ports});\nend entity;\n\narchitecture gates of {c.name}_gates is\n'
 if signals: ge+='  signal '+', '.join(signals)+' : std_logic;\n'
 ge+='begin\n'
 for kind,out,args in c.gates:
  expr=f'not {args[0]}' if kind=='NOT' else f'not ({args[0]} {"and" if kind=="NAND" else "or"} {args[1]})'
  ge+=f'  {out} <= {expr} after 1 ns;\n'
 ge+='end architecture;\n'
 (R/'testbench'/f'{c.name}_gates.vhd').write_text(header+ge)
# Sequential input steps: 30 ns settling, no simultaneous data/clock changes at sampling edge.
tests={
'rs_latch':[(dict(s=0,r=1),0,1,'Reset'),(dict(s=0,r=0),0,1,'Hold 0'),(dict(s=1,r=0),1,0,'Set'),(dict(s=0,r=0),1,0,'Hold 1'),(dict(s=1,r=1),0,0,'Forbidden'),(dict(s=0,r=1),0,1,'Recover via Reset'),(dict(s=0,r=0),0,1,'Hold after recovery')],
'd_latch':[(dict(d=0,en=1),0,1,'Initialize transparent'),(dict(d=1,en=1),1,0,'Follow 1'),(dict(d=1,en=0),1,0,'Close latch'),(dict(d=0,en=0),1,0,'Hold despite D change'),(dict(d=0,en=1),0,1,'Follow 0'),(dict(d=0,en=0),0,1,'Close at 0'),(dict(d=1,en=0),0,1,'Hold 0'),(dict(d=1,en=1),1,0,'Follow again')],
'd_ff':[(dict(d=0,clk=0),None,None,'Prepare D=0'),(dict(d=0,clk=1),0,1,'Rising captures 0'),(dict(d=1,clk=1),0,1,'High phase holds'),(dict(d=1,clk=0),0,1,'Falling holds'),(dict(d=0,clk=0),0,1,'Low phase change'),(dict(d=1,clk=0),0,1,'Prepare D=1'),(dict(d=1,clk=1),1,0,'Rising captures 1'),(dict(d=0,clk=1),1,0,'High phase holds 1'),(dict(d=0,clk=0),1,0,'Falling holds 1'),(dict(d=0,clk=1),0,1,'Rising captures 0')],
'jk_ff':[(dict(j=0,k=1,clk=0),None,None,'Prepare Reset'),(dict(j=0,k=1,clk=1),0,1,'Reset'),(dict(j=0,k=0,clk=1),0,1,'High holds'),(dict(j=0,k=0,clk=0),0,1,'Prepare Hold'),(dict(j=0,k=0,clk=1),0,1,'Hold 0'),(dict(j=1,k=0,clk=0),0,1,'Prepare Set'),(dict(j=1,k=0,clk=1),1,0,'Set'),(dict(j=0,k=0,clk=0),1,0,'Prepare Hold 1'),(dict(j=0,k=0,clk=1),1,0,'Hold 1'),(dict(j=1,k=1,clk=0),1,0,'Prepare Toggle'),(dict(j=1,k=1,clk=1),0,1,'Toggle to 0'),(dict(j=1,k=1,clk=0),0,1,'Falling holds'),(dict(j=1,k=1,clk=1),1,0,'Toggle to 1'),(dict(j=0,k=1,clk=0),1,0,'Prepare Reset again'),(dict(j=0,k=1,clk=1),0,1,'Reset again')],
'd_ff_async':[(dict(d=0,clk=0,set=0,clr=1),0,1,'Async Clear at low'),(dict(d=0,clk=0,set=1,clr=1),0,1,'Clear wins both high'),(dict(d=0,clk=0,set=1,clr=0),1,0,'Async Set no edge'),(dict(d=0,clk=0,set=0,clr=0),1,0,'Release Set holds'),(dict(d=0,clk=1,set=0,clr=0),0,1,'Normal rising captures 0'),(dict(d=1,clk=1,set=0,clr=0),0,1,'High D change holds'),(dict(d=1,clk=1,set=1,clr=0),1,0,'Async Set while high'),(dict(d=1,clk=1,set=1,clr=1),0,1,'Async Clear overrides Set'),(dict(d=1,clk=1,set=0,clr=1),0,1,'Clear maintained'),(dict(d=1,clk=1,set=0,clr=0),0,1,'Release Clear no edge'),(dict(d=1,clk=0,set=0,clr=0),0,1,'Falling holds'),(dict(d=1,clk=1,set=0,clr=0),1,0,'Normal rising captures 1'),(dict(d=1,clk=0,set=0,clr=0),1,0,'Return low')]}
for c in cs:
 rows=tests[c.name];pins=c.inputs+['q','qb'];txt=' '.join(pins+['<set>','<seq>'])+'\n'
 for n,(vals,q,qb,desc) in enumerate(rows,1): txt+=' '.join([str(vals[i]) for i in c.inputs]+['<DC>' if v is None else str(v) for v in [q,qb]]+['1',str(n)])+' # '+desc+'\n'
 (R/'tests'/f'{c.name}.txt').write_text(txt)
 tb=header+'use std.env.all;\n\n'+f'entity tb_{c.name} is end;\narchitecture test of tb_{c.name} is\n'
 tb+='  signal '+', '.join(c.inputs)+" : std_logic := '0';\n  signal q, qb, gq, gqb : std_logic;\nbegin\n"
 tb+=f'  dut: entity work.{c.name}(rtl) port map('+', '.join(c.inputs+['q','qb'])+');\n'
 tb+=f'  net: entity work.{c.name}_gates(gates) port map('+', '.join(c.inputs+['gq','gqb'])+');\n  process\n  begin\n'
 for n,(vals,q,qb,desc) in enumerate(rows,1):
  tb+='    '+ ' '.join(f"{i} <= '{vals[i]}';" for i in c.inputs)+'\n    wait for 30 ns;\n'
  if q is not None:
   tb+=f'''    assert q = '{q}' and qb = '{qb}' report "RTL step {n}: {desc}" severity failure;
    assert gq = '{q}' and gqb = '{qb}' report "Gates step {n}: {desc}" severity failure;
    assert q = gq and qb = gqb report "Equivalence step {n}" severity failure;
'''
  tb+=f'    report "PASS step {n}: {desc}" severity note;\n'
 tb+=f'    report "ALL PASS {c.name}" severity note;\n    finish;\n    wait;\n  end process;\nend architecture;\n'
 (R/'testbench'/f'tb_{c.name}.vhd').write_text(tb)
# Actual Logisim schematics: every storage element is individual gates, nets joined by labeled tunnels.
def attr(e,n,v): E.SubElement(e,'a',name=n,val=str(v))
def comp(parent,lib,name,x,y,**attrs):
 e=E.SubElement(parent,'comp',lib=str(lib),name=name,loc=f'({x},{y})')
 for k,v in attrs.items():attr(e,k,v)
 return e
root=E.Element('project',source='5.0.0',version='1.0')
for i,n in enumerate(['Wiring','Gates','Plexers','Arithmetic','Memory','I/O','Base']):E.SubElement(root,'lib',name=str(i),desc='#'+n)
E.SubElement(root,'main',name='rs_latch');opt=E.SubElement(root,'options');attr(opt,'simlimit',10000)
for c in cs:
 cir=E.SubElement(root,'circuit',name=c.name);attr(cir,'appearance','logisim_evolution')
 for i,pin in enumerate(c.inputs):
  x,y=100,100+i*60;comp(cir,0,'Pin',x,y,label=pin,appearance='classic');comp(cir,0,'Tunnel',x+40,y,label=pin,facing='west');E.SubElement(cir,'wire',{'from':f'({x},{y})','to':f'({x+40},{y})'})
 for i,pin in enumerate(c.outputs):
  x,y=400,100+i*60;comp(cir,0,'Pin',x,y,label=pin,type='output',facing='west',appearance='classic');comp(cir,0,'Tunnel',x-40,y,label=pin,facing='east');E.SubElement(cir,'wire',{'from':f'({x-40},{y})','to':f'({x},{y})'})
 for n,(kind,out,args) in enumerate(c.gates):
  col=n//6;row=n%6;x=260+col*300;y=380+row*110
  comp(cir,1,kind+' Gate',x,y,size=30 if kind=='NOT' else 50,label=f'G{n+1}',**({} if kind=='NOT' else {'inputs':2}))
  for i,a in enumerate(args):
   ix=x-(30 if kind=='NOT' else 60);iy=y+(0 if kind=='NOT' else (-20 if i==0 else 20));tx=ix-30
   comp(cir,0,'Tunnel',tx,iy,label=a,facing='east');E.SubElement(cir,'wire',{'from':f'({tx},{iy})','to':f'({ix},{iy})'})
  comp(cir,0,'Tunnel',x+40,y,label=out,facing='west');E.SubElement(cir,'wire',{'from':f'({x},{y})','to':f'({x+40},{y})'})
 E.SubElement(cir,'comp',lib='6',name='Text',loc='(100,300)')
 t=cir[-1];attr(t,'text',c.name+' | Gate-level only | Same-name tunnels are connected');attr(t,'halign','left')
E.indent(root);E.ElementTree(root).write(R/'logisim'/'sequential_logic.circ',encoding='utf-8',xml_declaration=True)
(R/'results'/'design.json').write_text(json.dumps([dict(name=c.name,inputs=c.inputs,gates=c.gates,tests=tests[c.name]) for c in cs],indent=2))
print('Created 5 RTL designs, 5 gate models, 5 testbenches, 5 vector files and gate-only Logisim project.')


