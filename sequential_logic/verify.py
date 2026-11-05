from pathlib import Path
import subprocess,json,sys,os,shutil
R=Path(__file__).resolve().parent
ghdl=os.environ.get('GHDL_EXE') or shutil.which('ghdl') or str(R/'tools/ghdl/bin/ghdl.exe')
java=os.environ.get('JAVA_EXE') or shutil.which('java') or str(next((R/'tools/jre').rglob('java.exe')))
jar=os.environ.get('LOGISIM_JAR','C:/Program Files/logisim-evolution/app/logisim-evolution-5.0.0-all.jar')
def run(args,log):
 p=subprocess.run(args,cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
 (R/'results'/log).write_text(p.stdout+p.stderr,encoding='utf-8');print(log, 'PASS' if p.returncode==0 else 'FAIL');return p
names=['rs_latch','d_latch','d_ff','jk_ff','d_ff_async']
for name in names:
 p=run([ghdl,'-a','--std=08',f'vhdl/{name}.vhd',f'testbench/{name}_gates.vhd',f'testbench/tb_{name}.vhd'],name+'_compile.log')
 if p.returncode:sys.exit(1)
 p=run([ghdl,'-r','--std=08','tb_'+name,'--assert-level=error',f'--vcd=results/{name}.vcd','--stop-time=2us'],name+'_simulation.log')
 if p.returncode:sys.exit(1)
 p=run([ghdl,'--synth','--std=08','--latches','--out=vhdl',name],name+'_synthesis.log')
 if p.returncode:sys.exit(1)
 (R/'synthesis'/f'{name}_netlist.vhd').write_text(p.stdout)
 net=p.stdout.replace('entity '+name+' is','entity '+name+'_synth is').replace('architecture rtl of '+name+' is','architecture rtl of '+name+'_synth is')
 (R/'tmp'/f'{name}_synth.vhd').write_text(net)
 tb=(R/'testbench'/f'tb_{name}.vhd').read_text().replace('entity work.'+name+'(rtl)','entity work.'+name+'_synth(rtl)').replace('tb_'+name,'tb_'+name+'_synth')
 (R/'tmp'/f'tb_{name}_synth.vhd').write_text(tb)
 p=run([ghdl,'-a','--std=08',f'tmp/{name}_synth.vhd',f'tmp/tb_{name}_synth.vhd'],name+'_netlist_compile.log')
 if p.returncode:sys.exit(1)
 p=run([ghdl,'-r','--std=08','tb_'+name+'_synth','--assert-level=error'],name+'_netlist_simulation.log')
 if p.returncode:sys.exit(1)
 p=run([ghdl,'--synth','--std=08','--latches','--out=raw',name],name+'_netlist_raw.log')
 if p.returncode:sys.exit(1)
 (R/'synthesis'/f'{name}_netlist.txt').write_text(p.stdout)
 p=run([java,'-Dfile.encoding=UTF-8','-Dsun.stdout.encoding=UTF-8','-Dsun.stderr.encoding=UTF-8','-jar',jar,'--locale','en','--test-vector',name,f'tests/{name}.txt','logisim/sequential_logic.circ'],name+'_logisim.log')
 if p.returncode or 'Failed: 0' not in p.stdout:sys.exit(1)
print('ALL 5 DESIGNS PASSED')


