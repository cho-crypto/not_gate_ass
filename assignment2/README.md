# VHDL Assignment-2

디지털논리회로설계 강의 자료 **VHDL_1, 22쪽 (1.4 Problems)**의 5문제를 구현했습니다.

## 제출 파일

- [PDF 보고서](report/assignment2_report.pdf)
- [Logisim 프로젝트](logisim/assignment2.circ) — Logisim-evolution 5.0.0
- [VHDL 소스](src/) — 문제별 5개 모듈과 보조 HEX 디코더
- [검증 로그 및 결과](results/)
- [테스트벤치와 Logisim 입력 벡터](tests/)
- [원문 대조 및 재검토 기록](REVIEW.md) — 테스트의 정확한 0/1 비교 보강, 독립 표시 검사 16,413개 추가 통과, 보조 VHDL 회로의 핀 간격 개선

| 문제 | VHDL | 동작 |
| --- | --- | --- |
| 1 | `and_or4.vhd` | 4입력 AND / OR |
| 2 | `mux8.vhd` | `s=000`은 `d(0)`, `s=111`은 `d(7)` 선택 |
| 3 | `letters7seg.vhd` | `sel=000..101`: A,b,C,d,F,G, `110/111`: 소등 |
| 4 | `voting25.vhd` | 25명 중 찬성 13명 이상일 때 `result=1` |
| 5 | `popcount13_display.vhd` | 13비트의 1 개수를 표시. `en=0`이면 소등 |
| 보조 | `hex7seg.vhd` | 0~F 전체 표시 패턴 검증 |

## 표시 규칙

`seg(7 downto 0) = a,b,c,d,e,f,g,dp`이며 1이면 켜지는 active-high 방식입니다. dp는 항상 0입니다. 문자 a,b,c,d,f,g는 7세그먼트 글꼴에서 A,b,C,d,F,G로 표현했습니다. G는 a,c,d,e,f,g 획을 사용하여 숫자 6과 같은 모양입니다.

13비트의 1 개수는 최대 13이므로 문제 5의 실제 표시 범위는 0~D입니다. E와 F는 이 입력으로 도달할 수 없어 보조 디코더에서 따로 검증했습니다. 동작은 클록 없는 조합논리입니다.

## 검증 결과

| 대상 | Questa | Logisim | 범위 |
| --- | ---: | ---: | --- |
| Q1 | 16 | 16 | 모든 입력 |
| Q2 | 2,048 | 2,048 | 데이터 256개 × 선택 8개 |
| Q3 | 8 | 8 | 모든 선택값 |
| Q4 | 8,791 | 8,791 | 모든 찬성 수, 회전 경계 패턴, 고정 난수 |
| Q5 | 16,384 | 16,384 | 입력 8,192개 × enable 2개 |
| HEX | 16 | — | 0~F |
| 합계 | **27,263** | **27,247** | **실패 0** |

Questa 2025.3 컴파일·시뮬레이션 오류와 경고는 모두 0개입니다. Q4는 전체 2^25 입력을 전수 검사하지 않았습니다. seed 20261027의 난수 8,192개와 패턴 입력을 합친 뒤 중복을 제거했습니다. 검증은 안정된 이진 입력 기준이며 실물 FPGA 검증은 수행하지 않았습니다.

## Logisim 실행

1. `logisim/assignment2.circ`를 엽니다.
2. 왼쪽 트리에서 `Q1_AND_OR`, `Q2_MUX8`, `Q3_LETTERS`, `Q4_VOTING25`, `Q5_COUNT_DISPLAY` 중 하나를 더블클릭합니다.
3. Poke(손) 도구로 입력 핀의 비트를 클릭해 변경합니다. 여러 비트 핀은 비트를 클릭하거나 0/1 키로 값을 입력할 수 있습니다.
4. 기본 Q1~Q5 회로는 Logisim 자체 부품으로 작성되어 외부 시뮬레이터 없이 실행됩니다.

VHDL을 직접 실행하는 `VHDL_` 접두사의 회로 5개도 포함했습니다. 이 회로는 프로젝트에 내장한 제출 소스와 연결되어 있습니다. 사용하려면 Logisim 설정에서 Questa/ModelSim 실행 경로를 지정하고 **Simulate > VHDL Simulation Enabled**를 켭니다. 이 PC의 Questa 경로는 `C:\altera_pro\26.1.1\questa_fse\win64`이며 다른 PC에서는 설치 위치를 사용합니다. 자동 검증 로그는 기본 Q1~Q5 회로의 실제 출력을 검사한 결과입니다.

JAR 실행 환경에서는 제출 폴더를 현재 디렉터리로 두고 다음과 같이 검사합니다.

```sh
java -jar /path/to/logisim-evolution-5.0.0-all.jar --test-vector Q1_AND_OR tests/Q1_AND_OR.txt logisim/assignment2.circ
```

나머지는 `Q1_AND_OR`와 해당 벡터 파일명을 Q2~Q5의 회로 이름으로 바꿉니다. `tests/run_logisim.py`에 JAR 경로를 전달하면 5개를 모두 실행하고 실패 여부를 확인합니다.

```sh
python tests/run_logisim.py /path/to/logisim-evolution-5.0.0-all.jar
```

## Questa 실행

`vsim`이 PATH에 있는 상태에서 **이 README가 있는 폴더**에서 실행합니다.

```sh
vsim -c -do tests/simulate.do -l results/questa_results.log
```

`ALL TESTS PASSED`와 종료 코드 0을 확인합니다. 이 명령은 로컬 `work/`, `modelsim.ini`, 파형 등 실행 파일을 생성할 수 있습니다. 테스트벤치는 VHDL-2008을 사용합니다.

## 참고

- 강의 자료: 한양대학교 디지털논리회로설계, `VHDL_1`, 22쪽.
- [강의 예제 코드](https://github.com/lizhuoh9/VHDL_code): 입출력 표기와 표시 순서를 참고했습니다. 제출 구현과 검증 벡터는 이번 문제에 맞춰 작성했습니다.

LMS에는 GitHub 계정 프로필이 아니라 이 과제를 포함한 **저장소 링크**를 제출합니다.
