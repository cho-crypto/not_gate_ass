"""Run all Logisim binary-reference vectors; usage: python tests/run_logisim.py JAR [JAVA]."""
from pathlib import Path
import subprocess,sys,re

root=Path(__file__).resolve().parents[1]
if len(sys.argv)<2:
    raise SystemExit('usage: python tests/run_logisim.py LOGISIM_JAR [JAVA_EXECUTABLE]')
jar=str(Path(sys.argv[1]).resolve())
java=sys.argv[2] if len(sys.argv)>2 else 'java'
failed=False
for name in ['Q1_AND_OR','Q2_MUX8','Q3_LETTERS','Q4_VOTING25','Q5_COUNT_DISPLAY']:
    p=subprocess.run([java,'-jar',jar,'--test-vector',name,f'tests/{name}.txt','logisim/assignment2.circ'],cwd=root,capture_output=True,timeout=180)
    text=(p.stdout+p.stderr).decode('utf-8',errors='replace')
    totals=re.findall(r'Passed:\s*(\d+),\s*Failed:\s*(\d+)',text)
    ok=p.returncode==0 and totals and int(totals[-1][1])==0
    print(f'{name}: '+(f'passed={totals[-1][0]}, failed={totals[-1][1]}' if totals else 'no result'))
    failed=failed or not ok
    if not ok:
        (root/'results'/f'{name}_rerun.log').write_text(text,encoding='utf-8')
raise SystemExit(1 if failed else 0)
