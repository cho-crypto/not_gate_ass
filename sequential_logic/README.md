# Sequential Logic Assignment

RS Latch, D Latch, positive-edge D Flip-Flop, JK Flip-Flop, and D Flip-Flop with asynchronous Set/Clear.

## 제출 파일

- `vhdl/`: 회로별 VHDL 소스 5개 (VHDL-2008)
- `logisim/sequential_logic.circ`: 개별 게이트로 구현한 5개 회로
- `output/pdf/sequential_logic_report.pdf`: 회로도, RTL 코드, 생성된 합성 회로도, 실제 파형 및 검증 표
- `testbench/`: 테스트벤치와 같은 게이트 연결로 작성한 지연 모델
- `tests/`: Logisim 순차 테스트 벡터
- `results/`: 실제 컴파일/시뮬레이션/합성/Logisim 로그와 VCD 파형
- `synthesis/`: GHDL이 생성한 VHDL 및 raw 합성 넷리스트
- `figures/`: 보고서에 포함된 회로도와 파형 이미지

## 검증 결과

| 회로 | Logisim 순차 벡터 | RTL + 게이트 모델 | 합성 넷리스트 재검증 |
|---|---:|---|---|
| RS Latch | 7/7 | PASS | PASS |
| D Latch | 8/8 | PASS | PASS |
| D Flip-Flop | 10/10 | PASS | PASS |
| JK Flip-Flop | 22/22 | PASS | PASS |
| Async Set/Clear D Flip-Flop | 13/13 | PASS | PASS |

총 60개 기본 벡터 중 D FF의 최초 준비 단계 1개만 미초기화 출력을 검사하지 않습니다. 나머지 59개 단계에서 Q와 Qb를 검사합니다. 수정 JK는 추가 4,984개 벡터와 내부 21개 출력 검사도 모두 통과했습니다. 테스트 실패 시 verify.py가 중단됩니다. Logisim은 벡터 실패에도 종료 코드가 0일 수 있으므로 `Failed: 0` 문구도 검사합니다.

## Logisim 사용법

1. Logisim-evolution 5.0.0으로 `logisim/sequential_logic.circ`를 엽니다.
2. 왼쪽 목록에서 회로를 선택합니다.
3. Poke 도구로 입력 Pin을 클릭합니다. tests/*.txt의 순서를 따라 초기화 후 확인합니다.
4. Simulate > Test Vector에서 해당 회로의 `tests/*.txt`를 불러오면 순서대로 자동 검증할 수 있습니다.

게이트와 배선만으로 동작하므로 **VHDL Simulation Enabled나 Questa 연결이 필요 없습니다.** 기본 Latch, Flip-Flop, Register 등의 저장 부품은 사용하지 않았습니다. 같은 이름의 Tunnel 단자는 전기적으로 연결되며 피드백도 이에 포함됩니다.

### 회로 구성

- RS: NOR 2개, Q = NOT(R OR Qb), Qb = NOT(S OR Q).
- D Latch: NAND 5개, 두 입력을 묶은 NAND로 D를 반전.
- D FF: Master D Latch(클록 0에서 열림), Slave D Latch(클록 1에서 열림), NOT 게이트. G2-G6은 Master, G7-G11은 Slave.
- JK FF: 활성 Low 비동기 Clear 입력 `clr_n` 추가. `clr_n=0`이면 데이터 경로를 차단하고 Master/Slave 모두 Q=0으로 초기화합니다. 시작 시 입력 기본값 0이므로 Clear가 적용됩니다. `clr_n=1`로 바꿔 정상 동작을 시험하세요. Dnext = J*Qb + (NOT K)*Q를 NAND로 구현하고 NAND Master-Slave에 입력. Q/Qb 피드백이 포함됨. 반전도 NAND로 구현.
- Async D FF: Master/Slave 모두 비동기 제어. clrn=NOT clr, setn=NOT(set AND clrn), idle=clrn AND setn. 제어 중에는 데이터 경로를 차단. clr가 set보다 우선.

## 주의할 동작

- JK는 시작 시 `clr_n=0`으로 Clear되어 Q=0,Qb=1이 됩니다. 다른 저장회로는 유효한 Reset/Set/쓰기/클록 에지로 초기화합니다.
- NOR RS에서 S=R=1이면 Q=Qb=0입니다. 두 입력을 동시에 0으로 해제한 상태는 보장할 수 없으므로 Reset을 거쳐 복구합니다.
- 비동기 set/clr은 클록 없이 동작합니다. 두 신호가 모두 1이면 Q=0, Qb=1입니다.
- 데이터와 클록에 setup/hold 여유를 둡니다. 게이트 모델의 1 ns 지연과 단계당 30 ns는 논리 검증용이며 실소자의 메타안정성/전파지연 분석이 아닙니다.

## 재현

검증 도구: GHDL 6.0.0 mcode, Logisim-evolution 5.0.0, Java 25.0.5. VHDL-2008 사용.

필요 도구가 PATH에 있으면 `GHDL_EXE`, `JAVA_EXE`를 생략할 수 있습니다. Logisim JAR 경로는 환경에 맞춰 지정합니다.

```powershell
$env:GHDL_EXE = 'C:/path/to/ghdl.exe'
$env:JAVA_EXE = 'C:/path/to/java.exe'
$env:LOGISIM_JAR = 'C:/path/to/logisim-evolution-5.0.0-all.jar'
python verify.py
```

개별 회로 실행 예:

```text
ghdl -a --std=08 vhdl/d_ff.vhd testbench/d_ff_gates.vhd testbench/tb_d_ff.vhd
ghdl -r --std=08 tb_d_ff --assert-level=error --vcd=results/d_ff.vcd
ghdl --synth --std=08 --latches --out=vhdl d_ff
java -jar logisim-evolution-5.0.0-all.jar --test-vector d_ff tests/d_ff.txt logisim/sequential_logic.circ
```

`--latches`는 RS/D Latch의 의도적인 저장/피드백을 허용합니다. 합성은 특정 FPGA에 매핑하기 전의 **범용 논리 합성**입니다. 생성된 VHDL 넷리스트도 동일한 테스트벤치에서 재검증했습니다. 기술 종속 FPGA 배치배선이나 타이밍 분석은 수행하지 않았습니다.

보고서 재생성: Python 패키지 `reportlab matplotlib pymupdf pillow`를 준비하고 `python build_report.py`를 실행합니다. `build_assignment.py`는 회로 파일과 테스트 소스를 다시 생성합니다.

## 도구 문서

- https://ghdl.github.io/ghdl/using/Synthesis.html
- https://github.com/logisim-evolution/logisim-evolution/blob/main/docs/test_vector.md

## JK 초기 E 개선 (2026-11-11)

기존 버전은 초기 E가 유효한 클록 입력 후 해제되었습니다. 수정본은 활성 Low Clear를 추가하여 클록 없이 초기화합니다. clk=1에서도 Clear가 우선하고, 높은 클록에서 Clear를 해제해도 Q는 다음 상승 에지까지 유지됩니다. 정상 JK의 Hold/Set/Reset/Toggle 기능은 유지됩니다.

추가 검증은 `python verify_jk_reset.py`로 재현합니다. 초기 J/K/CLK 8조합, 비동기 Clear와 해제, 반복 토글 및 높은 클록 유지가 포함됩니다. `results/jk_ff_stress_logisim.log`와 `results/jk_ff_stress_internal.log`에 각각 4,984개 통과 기록이 있습니다.
