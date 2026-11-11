# VHDL 과제

## Sequential Logic Assignment

RS Latch, D Latch, D Flip-Flop, JK Flip-Flop, 비동기 Set/Clear D Flip-Flop의 게이트 및 VHDL 구현입니다.

- [이번 과제 제출 폴더](sequential_logic/)
- [PDF 보고서](sequential_logic/output/pdf/sequential_logic_report.pdf)
- [VHDL 소스 5개](sequential_logic/vhdl/)
- [게이트 기반 Logisim 프로젝트](sequential_logic/logisim/sequential_logic.circ)
- [테스트벤치](sequential_logic/testbench/)
- [시뮬레이션 파형과 검증 로그](sequential_logic/results/)
- [생성된 합성 넷리스트](sequential_logic/synthesis/)

Logisim 60개 기본 순차 벡터 및 수정 JK 추가 4,984개 벡터 통과. VHDL RTL, 게이트 모델 및 합성 넷리스트의 동작을 검증했습니다.
D FF 최초 준비 벡터 1개를 제외한 기본 59개 단계에서 Q와 Qb를 검사했습니다. JK에 활성 Low 비동기 Clear(`clr_n`)를 추가했으며, 시작 시 0으로 초기화하고 1로 해제해 사용합니다. 내부 21개 출력도 4,984단계에서 모두 정상값을 확인했습니다.


## Assignment-2 (VHDL_1)

강의 자료 VHDL_1의 5문제: 4입력 AND/OR, 8:1 MUX, 문자 표시, 25인 투표기, 13비트 1 개수 표시.

- [과제 설명 및 실행 방법](assignment2/README.md)
- [PDF 보고서](assignment2/report/assignment2_report.pdf)
- [VHDL 소스](assignment2/src/)
- [Logisim 프로젝트](assignment2/logisim/assignment2.circ)
- [검증 결과](assignment2/results/)

Questa 27,263개, Logisim 27,247개 테스트 통과. 자세한 검증 범위는 보고서에 기재했습니다.

## 기존 NOT 게이트 과제

- [기존 제출물](submission/)
