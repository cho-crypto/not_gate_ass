from pathlib import Path
import itertools,random,subprocess,json,xml.etree.ElementTree as E
R=Path(__file__).resolve().parent;java=str(next((R/'tools/jre').rglob('java.exe')))
rows=[];rng=random.Random(1111)
for sid,(j,k,clk) in enumerate(itertools.product([0,1],repeat=3),1):
 seq=[]
 def add(j,k,clk,clr,q,label):seq.append((j,k,clk,clr,q,label))
 add(j,k,clk,0,0,'Cold reset');add(j,k,clk,0,0,'Reset holds');add(j,k,clk,1,0,'Release reset')
 q=0
 for cycle in range(100):
  j,k=(1,1) if cycle<50 else (rng.randrange(2),rng.randrange(2))
  add(j,k,0,1,q,'Falling/prepare')
  add(j,k,0,1,q,'Low hold')
  q=int((j and not q) or (not k and q));add(j,k,1,1,q,'Rising')
  for rep in range(3):add(j,k,1,1,q,'High hold')
  if cycle%10==0:
   add(1,1,1,0,0,'Async clear at high');add(1,1,1,1,0,'Release clear high');q=0
 for n,data in enumerate(seq,1):rows.append((*data,sid,n))
header='j k clk clr_n q qb <set> <seq>\n';txt=header
for j,k,clk,clr,q,label,sid,n in rows:txt+=f'{j} {k} {clk} {clr} {q} {1-q} {sid} {n} # {label}\n'
(R/'tests/jk_ff_stress.txt').write_text(txt)
args=[java,'-Dfile.encoding=UTF-8','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8','-jar','C:/Program Files/logisim-evolution/app/logisim-evolution-5.0.0-all.jar','--locale','en','--test-vector','jk_ff','tests/jk_ff_stress.txt','logisim/sequential_logic.circ']
p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf-8',timeout=120);(R/'results/jk_ff_stress_logisim.log').write_text(p.stdout+p.stderr,encoding='utf-8');print([l for l in p.stdout.splitlines() if 'Passed:' in l]);assert 'Failed: 0' in p.stdout
# Observe every internal gate output using a temporary copy, with unchanged logic.
tree=E.parse(R/'logisim/sequential_logic.circ');c=tree.getroot().find("circuit[@name='jk_ff']")
gates=next(d['gates'] for d in json.loads((R/'results/design.json').read_text()) if d['name']=='jk_ff');internal=[o for _,o,_ in gates if o not in ['q','qb']]
for i,name in enumerate(internal):
 y=100+i*60;pin=E.SubElement(c,'comp',lib='0',name='Pin',loc=f'(2000,{y})')
 for k,v in [('type','output'),('facing','west'),('label','mon_'+name)]:E.SubElement(pin,'a',name=k,val=v)
 t=E.SubElement(c,'comp',lib='0',name='Tunnel',loc=f'(1960,{y})');E.SubElement(t,'a',name='label',val=name);E.SubElement(t,'a',name='facing',val='east');E.SubElement(c,'wire',{'from':f'(1960,{y})','to':f'(2000,{y})'})
tree.write(R/'tmp/jk_monitored.circ',encoding='utf-8',xml_declaration=True)
txt='j k clk clr_n q qb '+' '.join('mon_'+v for v in internal)+' <set> <seq>\n';mq=0
for j,k,clk,clr,q,label,sid,n in rows:
 if not clr:mq=0
 elif not clk:mq=int((j and not q) or (not k and q))
 env=dict(j=j,k=k,clk=clk,clr_n=clr,q=q,qb=1-q,mq=mq,mqb=1-mq)
 for _ in range(30):
  for kind,out,(a,b) in gates:
   if out not in ['q','qb','mq','mqb'] and a in env and b in env:env[out]=int(not(env[a] and env[b]))
 assert all(env[o]==int(not(env[a] and env[b])) for _,o,(a,b) in gates)
 txt+=' '.join(map(str,[j,k,clk,clr,q,1-q]+[env[v] for v in internal]+[sid,n]))+'\n'
(R/'tmp/jk_internal.txt').write_text(txt)
args[-2:]=['tmp/jk_internal.txt','tmp/jk_monitored.circ'];p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf-8',timeout=120);(R/'results/jk_ff_stress_internal.log').write_text(p.stdout+p.stderr,encoding='utf-8');print('Internal nets:',len(internal),[l for l in p.stdout.splitlines() if 'Passed:' in l]);assert 'Failed: 0' in p.stdout
print('ALL RESET STRESS CHECKS PASSED; vectors',len(rows))
