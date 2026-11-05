library ieee;
use ieee.std_logic_1164.all;
entity jk_ff is
  port (
    j: in std_logic;
    k: in std_logic;
    clk: in std_logic;
    q, qb: out std_logic
  );
end entity;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

architecture rtl of jk_ff is
  signal wrap_j: std_logic;
  signal wrap_k: std_logic;
  signal wrap_clk: std_logic;
  signal wrap_q: std_logic;
  signal wrap_qb: std_logic;
  signal q_i : std_logic;
  signal n5 : std_logic;
  signal n6 : std_logic;
  signal n7 : std_logic;
  signal n8 : std_logic;
  signal n9 : std_logic;
  signal n10 : std_logic;
  signal n11 : std_logic;
  signal n13 : std_logic;
  signal n15 : std_logic;
  signal n18 : std_logic;
  signal n19 : std_logic;
begin
  wrap_j <= j;
  wrap_k <= k;
  wrap_clk <= clk;
  q <= wrap_q;
  qb <= wrap_qb;
  wrap_q <= q_i;
  wrap_qb <= n18;
  -- vhdl/jk_ff.vhd:14:10
  q_i <= n19; -- (signal)
  -- vhdl/jk_ff.vhd:19:12
  n5 <= not wrap_j;
  -- vhdl/jk_ff.vhd:19:18
  n6 <= wrap_k and n5;
  -- vhdl/jk_ff.vhd:20:27
  n7 <= not wrap_k;
  -- vhdl/jk_ff.vhd:20:21
  n8 <= n7 and wrap_j;
  -- vhdl/jk_ff.vhd:21:21
  n9 <= wrap_k and wrap_j;
  -- vhdl/jk_ff.vhd:21:45
  n10 <= not q_i;
  -- vhdl/jk_ff.vhd:21:7
  n11 <= q_i when n9 = '0' else n10;
  -- vhdl/jk_ff.vhd:20:7
  n13 <= n11 when n8 = '0' else '1';
  -- vhdl/jk_ff.vhd:19:7
  n15 <= n13 when n6 = '0' else '0';
  -- vhdl/jk_ff.vhd:25:19
  n18 <= not q_i;
  -- vhdl/jk_ff.vhd:18:5
  process (wrap_clk)
  begin
    if rising_edge (wrap_clk) then
      n19 <= n15;
    end if;
  end process;
end rtl;
