from pathlib import Path
import re,math,json,zipfile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch,Circle,Rectangle
from matplotlib.path import Path as MP
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import pymupdf
R=Path(__file__).resolve().parent
D=json.loads((R/'results/design.json').read_text(encoding='utf-8-sig'))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
NAVY='#173958';GREEN='#14816c';BLUE='#2868a9';GRAY='#64748b'
def save(fig,path):fig.savefig(path,dpi=180,bbox_inches='tight',facecolor='white');plt.close(fig)
def gatefig(c):
 n=len(c['gates']);cols=1 if n<=6 else (2 if n<=12 else (3 if n<=18 else 4));rows=math.ceil(n/cols)
 fig,ax=plt.subplots(figsize=(cols*4.1,max(3,rows*1.28+1)));ax.set_xlim(-.3,cols*4.1);ax.set_ylim(-.5,rows*1.28+.65);ax.axis('off')
 ax.text(0,rows*1.28+.3,'IN: '+', '.join(c['inputs'])+'     OUT: q, qb',color=NAVY,fontsize=12,weight='bold')
 for idx,(kind,out,args) in enumerate(c['gates']):
  col=idx//rows;row=idx%rows;x=col*4.1+1.6;y=(rows-row-1)*1.28+.25
  if kind=='NAND':
   p=MP([(x-.6,y-.3),(x-.15,y-.3),(x+.5,y-.3),(x+.5,y+.3),(x-.15,y+.3),(x-.6,y+.3),(x-.6,y-.3)],[1,2,4,4,4,2,2]);ax.add_patch(PathPatch(p,fill=False,lw=1.7,color=NAVY))
  elif kind=='NOR':
   p=MP([(x-.65,y-.3),(x-.15,y-.3),(x+.2,y-.25),(x+.4,y),(x+.2,y+.25),(x-.15,y+.3),(x-.65,y+.3),(x-.3,y),(x-.65,y-.3)],[1,4,4,4,4,4,4,3,3]);ax.add_patch(PathPatch(p,fill=False,lw=1.7,color=NAVY))
  else:
   ax.plot([x-.6,x+.4,x-.6,x-.6],[y-.3,y,y+.3,y-.3],color=NAVY,lw=1.7)
  ax.add_patch(Circle((x+.48,y),.08,fill=False,lw=1.5,color=NAVY))
  ys=[y] if len(args)==1 else [y+.18,y-.18]
  for a,yy in zip(args,ys):
   ax.plot([x-1.05,x-.53],[yy,yy],color=BLUE,lw=1.2);ax.text(x-1.12,yy,a,ha='right',va='center',fontsize=10,color=BLUE)
  ax.plot([x+.56,x+.9],[y,y],color=GREEN,lw=1.4);ax.text(x+.95,y,out,va='center',fontsize=10,color=GREEN)
  ax.text(x-.1,y+.48,f'G{idx+1}  {kind}',ha='center',fontsize=9,color=GRAY)
 ax.text(0,-.35,'Matching net labels are connected (Logisim tunnels), including all feedback paths.',fontsize=10,color=GRAY)
 save(fig,R/'figures'/f'{c["name"]}_gates.png')
def vcd_read(path):
 lines=path.read_text(encoding='utf-8-sig').splitlines();names={};vals={};tm=0;scale=1e-6;in_scale=False
 for line in lines:
  if '$timescale' in line:in_scale=True
  if in_scale:
   m=re.search(r'(\d+)\s*(fs|ps|ns)',line)
   if m:scale=int(m[1])*{'fs':1e-6,'ps':1e-3,'ns':1}[m[2]];in_scale=False
  if line.startswith('$var'):
   parts=line.split();name=parts[4]
   if name not in names:names[name]=parts[3];vals[parts[3]]=[]
  if line.startswith('#'):tm=int(line[1:])*scale
  elif line and line[0] in '01xXzZuU' and line[1:] in vals: vals[line[1:]].append((tm,line[0].lower()))
 return names,vals,tm

def wavefig(c):
 names,vals,end=vcd_read(R/'results'/f'{c["name"]}.vcd');sig=c['inputs']+['q','qb','gq','gqb']
 fig,axes=plt.subplots(len(sig),1,figsize=(14,len(sig)*.42+1.1),sharex=True)
 for i,(ax,name) in enumerate(zip(axes,sig)):
  data=vals[names[name]];xs=[t for t,v in data]+[end];ys=[float(v) if v in '01' else float('nan') for t,v in data];ys+=[ys[-1]]
  color=GREEN if name.startswith('g') else BLUE
  ax.step(xs,ys,where='post',lw=1.5,color=color);ax.set_ylim(-.25,1.25);ax.set_yticks([0,1]);ax.set_ylabel(name,rotation=0,labelpad=25,va='center',fontsize=10)
  ax.grid(axis='x',alpha=.18);ax.spines[['top','right']].set_visible(False);ax.tick_params(axis='y',labelsize=7)
  for t in range(30,int(end)+1,30):ax.axvline(t,color='#aab7c5',lw=.45,ls=':')
 axes[-1].set_xlabel('Time (ns)');axes[-1].set_xlim(0,end);axes[-1].set_xticks(range(0,int(end)+1,30));fig.suptitle(c['name']+' | GHDL simulation: RTL q/qb and delayed gate model gq/gqb',fontsize=12,color=NAVY)
 fig.tight_layout();save(fig,R/'figures'/f'{c["name"]}_waveform.png')

def synthfig(c):
 raw=(R/'synthesis'/f'{c["name"]}_netlist.txt').read_text(encoding='utf-8-sig');cells=[]
 pattern=r'(?:\\\w+|%\d+):\$\w+\{(n\d+w\d+)\}\s*:=\s*\$(\w+)\{i(\d+)\}\s*\('
 for m in re.finditer(pattern,raw):
  start=m.end();depth=1;k=start
  while depth:
   depth+= (raw[k]=='(')-(raw[k]==')');k+=1
  body=raw[start:k-1];ports=[];depth=0;i=0
  while i<len(body):
   if body[i]=='(':depth+=1
   elif body[i]==')':depth-=1
   if depth==0 and body.startswith('.$',i):
    pm=re.match(r'\.\$(\w+)\{p\d+\}:\s*',body[i:])
    if pm:
     rem=body[i+pm.end():];nm=re.search(r'\{(n\d+w\d+)\}',rem)
     cv=re.match(r"1'uh([01])",rem)
     val=('const'+cv[1]) if cv else (nm[1].replace('w1','') if nm else '?')
     ports.append((pm[1],val))
   i+=1
  cells.append((m[2],m[1].replace('w1',''),ports))
 n=len(cells);cols=1 if n<=5 else (2 if n<=12 else 3);rows=math.ceil(n/cols)
 fig,ax=plt.subplots(figsize=(cols*4.8,rows*1.1+1));ax.axis('off');ax.set_xlim(0,cols*4.8);ax.set_ylim(-.1,rows*1.1+.7)
 ins=re.findall(r'input \\(\w+);',raw)
 # Record physical input names and raw-net references from their usages.
 mappings=[]
 for name in ins:
  match=re.search(r'\\'+re.escape(name)+r'\{(n\d+w\d+)\}',raw)
  if match:mappings.append(name+'='+match[1].replace('w1',''))
 ax.text(.1,rows*1.1+.35,'INPUT NETS: '+', '.join(mappings),fontsize=10,color=NAVY)
 for idx,(kind,out,ports) in enumerate(cells):
  col=idx//rows;row=idx%rows;x=col*4.8+.1;y=(rows-row-1)*1.1+.1
  ax.add_patch(Rectangle((x+1.7,y),1.25,.72,facecolor='#edf3f8',edgecolor=NAVY,lw=1.1))
  ax.text(x+2.325,y+.36,'$'+kind,ha='center',va='center',fontsize=10,weight='bold',color=NAVY)
  for j,(p,net) in enumerate(ports):
   yy=y+.62-j*.16;ax.plot([x+1.4,x+1.7],[yy,yy],color=BLUE,lw=1);ax.text(x+1.35,yy,p+': '+net,ha='right',va='center',fontsize=8)
  ax.plot([x+2.95,x+3.2],[y+.36,y+.36],color=GREEN);ax.text(x+3.28,y+.36,out,va='center',fontsize=9,color=GREEN)
 outs=re.findall(r'\\(q|qb) := [^\n]*?\{(n\d+w\d+)\}',raw)
 ax.text(.1,-.06,'OUTPUT NETS: '+', '.join(k+'='+v.replace('w1','') for k,v in outs)+' | Same net IDs are wired together.',fontsize=9,color=GRAY)
 save(fig,R/'figures'/f'{c["name"]}_synthesis.png')
for c in D:gatefig(c);wavefig(c);synthfig(c)
# PDF in Korean, with code/net names preserved in ASCII.
pdfmetrics.registerFont(TTFont('KR','C:/Windows/Fonts/malgun.ttf'));pdfmetrics.registerFont(TTFont('KRB','C:/Windows/Fonts/malgunbd.ttf'))
W,H=841.89,595.28;P=R/'output/pdf/sequential_logic_report.pdf';cv=canvas.Canvas(str(P),pagesize=(W,H));cv.setTitle('순차논리회로 5종 구현 및 검증');page=0

def text(x,y,s,size=10,bold=False,color=NAVY):cv.setFillColor(HexColor(color));cv.setFont('KRB' if bold else 'KR',size);cv.drawString(x,y,s)
def head(title,sub):
 global page
 page+=1;cv.setFillColor(HexColor(NAVY));cv.rect(0,H-70,W,70,fill=1,stroke=0);text(32,H-31,title,20,True,'#ffffff');text(32,H-53,sub,9,False,'#e0eaf4');text(32,18,'순차논리회로 | VHDL-2008 / GHDL 6.0.0 / Logisim-evolution 5.0.0',8);text(W-55,18,str(page),8)
def imagefit(path,x,y,w,h):cv.drawImage(str(path),x,y,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
def lines(x,y,seq,size=10,gap=17):
 for s in seq:text(x,y,s,size);y-=gap
 return y

titles={'rs_latch':'RS Latch','d_latch':'D Latch','d_ff':'Positive-edge D Flip-Flop','jk_ff':'Positive-edge JK Flip-Flop','d_ff_async':'D Flip-Flop with Asynchronous Set/Clear'}
notes={
'rs_latch':['NOR 게이트 2개의 출력을 서로 반대쪽 입력으로 연결하여 상태를 저장한다.','S=1,R=0: Set / S=0,R=1: Reset / S=0,R=0: Hold.','S=R=1에서는 Q=Qb=0이 되어 상보 관계가 깨진다. 금지 상태이다.','금지 상태에서 두 입력을 동시에 해제한 결과는 보장하지 않는다. Reset을 거쳐 복구한다.'],
'd_latch':['D의 반전과 입력 게이팅, 교차 결합 NAND 쌍으로 총 5개의 NAND 게이트를 사용한다.','en=1에서는 Q가 D를 따라가며, en=0에서는 이전 값을 유지한다.','반전은 NAND의 두 입력을 묶어 구현했다. 기본 Latch 부품은 사용하지 않았다.'],
'd_ff':['Master는 clk=0에서 열리고, Slave는 clk=1에서 열린다. 두 래치와 인버터로 구성했다.','clk 상승 에지에서 Master에 저장된 D가 Slave로 전달된다.','D가 클록의 높은 구간 또는 낮은 구간에서 바뀌어도 최종 Q는 다음 상승 에지까지 유지된다.'],
'jk_ff':['다음 상태식 Dnext = J·Qb + (NOT K)·Q를 NAND 게이트로 구현했다.','Q와 Qb를 입력 논리에 피드백하고, NAND Master-Slave 구조로 상승 에지에서만 저장한다.','J,K=00: Hold / 10: Set / 01: Reset / 11: Toggle. clk 반전도 NAND로 구성했다.','Toggle은 에지당 한 번만 발생한다. 레벨 민감 JK 래치의 반복 토글을 피한다.'],
'd_ff_async':['Clear를 먼저 적용하고, Set은 Clear가 0일 때만 유효하도록 구성했다.','clrn=NOT clr, setn=NOT(set AND clrn), idle=clrn AND setn.','비동기 제어 중에는 데이터 경로를 차단하고 Master와 Slave 모두에 동일한 제어를 적용한다.','Clear와 Set은 클록 에지를 기다리지 않는다. 두 신호가 0이면 정상 D 플립플롭으로 동작한다.']}
head('순차논리회로 5종 구현 및 검증','RS Latch / D Latch / D Flip-Flop / JK Flip-Flop / Asynchronous Set-Clear D Flip-Flop')
lines(38,490,['1. 과제 목적', '게이트 수준 Logisim 회로와 VHDL 구현이 같은 논리 기능을 수행하는지 검증한다.'],12,24)
text(38,413,'2. 구현 및 검증 방법',13,True)
lines(38,389,['Logisim: 개별 NOR/NAND/NOT 게이트와 Tunnel 배선만 사용. 기본 Latch/Flip-Flop 부품 없음.','VHDL: RTL 소스 5개를 작성하고 GHDL에서 컴파일, 시뮬레이션 및 범용 논리 합성을 수행.','합성된 VHDL 넷리스트도 다시 컴파일하고 동일한 테스트벤치로 재검증했다.','게이트 모델: Logisim과 같은 게이트 연결에 1 ns 지연을 주고 RTL과 출력을 비교했다.','파형은 실제 GHDL VCD에서 생성했고, 회로도는 제출 회로/합성 넷리스트에서 생성했다.'],10,22)
text(38,263,'3. 결과 요약',13,True)
for i,c in enumerate(D):
 y=237-i*24;name=c['name'];count=len(c['tests']);text(45,y,f'{titles[name]:48s}',10);text(440,y,f'Logisim {count}/{count} PASS | RTL / Gates / Synth PASS',10,True,GREEN)
lines(38,91,['초기 상태는 보장하지 않는다. RS는 Reset, D Latch는 en=1에서 D=0,','D/JK 플립플롭은 유효한 첫 상승 에지, 비동기 D 플립플롭은 Clear로 초기화한다.'],9,15)
cv.showPage()
for num,c in enumerate(D,1):
 name=c['name'];head(f'{num}. {titles[name]} - 게이트 회로','Logisim gate-level implementation | All matching tunnel labels are electrically connected')
 y=lines(34,505,notes[name],10,18)
 imagefit(R/'figures'/f'{name}_gates.png',32,48,W-64,y-62)
 cv.showPage()
 head(f'{num}. {titles[name]} - VHDL 및 합성','Synthesized schematic generated from GHDL raw netlist | Generic synthesis, not FPGA place-and-route')
 text(32,503,'VHDL RTL',12,True)
 code=(R/'vhdl'/f'{name}.vhd').read_text(encoding='utf-8-sig').splitlines();font=9.0
 for i,line in enumerate(code):cv.setFont('Courier',font);cv.setFillColor(HexColor(NAVY));cv.drawString(32,480-i*12.5,line)
 text(375,503,'생성된 합성 회로도',12,True)
 imagefit(R/'figures'/f'{name}_synthesis.png',370,92,440,394)
 lines(32,66,['합성 셀: $dlatch / $dff / $adff 및 조합논리. 출력 Qb는 Q의 반전이며 RS 금지 상태는 예외이다.','넷 ID가 같은 단자는 연결되어 있다. 전체 연결 정보는 synthesis/*_netlist.txt 및 .vhd에 포함했다.'],8,14)
 cv.showPage()
 head(f'{num}. {titles[name]} - 시뮬레이션 결과','Actual VCD waveform | q/qb: RTL outputs, gq/gqb: delayed gate-model outputs')
 imagefit(R/'figures'/f'{name}_waveform.png',30,300,782,224)
 # Results table from verified stimuli. Mark each comparison only after checking logs.
 log=(R/'results'/f'{name}_logisim.log').read_text(encoding='utf-8-sig');assert f'Passed: {len(c["tests"])}, Failed: 0' in log
 assert 'ALL PASS '+name in (R/'results'/f'{name}_simulation.log').read_text(encoding='utf-8-sig')
 assert 'ALL PASS '+name in (R/'results'/f'{name}_netlist_simulation.log').read_text(encoding='utf-8-sig')
 text(38,283,'Step     입력 ('+', '.join(c['inputs'])+')                  Q / Qb       확인 동작                                      결과',9,True)
 rowheight=min(16,225/len(c['tests']))
 for i,(vals,q,qb,desc) in enumerate(c['tests']):
  yy=262-i*rowheight;iv=', '.join(str(vals[k]) for k in c['inputs']);ov='unchecked' if q is None else f'{q} / {qb}'
  text(40,yy,str(i+1),8);text(90,yy,iv,8);text(262,yy,ov,8);text(365,yy,desc,8);text(730,yy,'PASS' if q is not None else 'INIT',8,True,GREEN)
 lines(38,45,['각 단계는 30 ns 유지 후 검사했다. 최초 미초기화 단계는 출력 비교를 제외했다.','1 ns 게이트 지연은 동작 검증용이며 실제 소자의 타이밍/메타안정성을 예측하는 값이 아니다.'],8,12)
 cv.showPage()
head('재현 방법 및 제출 파일','Reproducible verification and deliverables')
lines(38,495,['1. Logisim','logisim/sequential_logic.circ를 열고 왼쪽에서 원하는 회로를 선택한다.','각 회로의 입력 Pin을 Poke 도구로 클릭한다. tests/*.txt 순서로 입력을 적용한다.','Simulate > Test Vector에서 해당 txt 파일을 불러오면 순차 테스트를 실행할 수 있다.','이 회로는 게이트만 사용하므로 VHDL Simulation Enabled 또는 Questa 연동이 필요 없다.','','2. VHDL 검증 및 합성','GHDL 6.0.0과 Java 21 이상을 준비한 뒤 README의 실행 명령을 사용한다.','verify.py는 RTL, 1 ns 게이트 모델, 합성 넷리스트, Logisim 순차 벡터를 검증한다.','results/에는 로그와 VCD 파형, synthesis/에는 생성된 범용 합성 넷리스트가 있다.','','3. 제출 구성','vhdl/*.vhd / testbench/*.vhd / logisim/*.circ / output/pdf/*.pdf','추가 검증 자료: tests/, results/, synthesis/, figures/, README.md.'],11,24)
lines(38,100,['참고 도구 문서','GHDL: https://ghdl.github.io/ghdl/using/Synthesis.html','Logisim Test Vector: https://github.com/logisim-evolution/logisim-evolution/blob/main/docs/test_vector.md'],8,16)
cv.showPage();cv.save()
# Render complete report for visual QA.
doc=pymupdf.open(P); thumbs=[]
for i,p in enumerate(doc):
 pix=p.get_pixmap(matrix=pymupdf.Matrix(1,1));pix.save(R/'tmp'/f'page_{i+1:02}.png')
print('PDF:',P,'pages:',len(doc))
from PIL import Image,ImageOps,ImageDraw
cards=[]
for i in range(len(doc)):
 im=Image.open(R/'tmp'/f'page_{i+1:02}.png').convert('RGB');im.thumbnail((420,300));can=Image.new('RGB',(440,325),'#cbd5e1');can.paste(im,((440-im.width)//2,5));ImageDraw.Draw(can).text((12,307),str(i+1),fill='black');cards.append(can)
contact=Image.new('RGB',(440*3,325*math.ceil(len(cards)/3)),'white')
for i,im in enumerate(cards):contact.paste(im,((i%3)*440,(i//3)*325))
contact.save(R/'tmp/report_contact.png')
