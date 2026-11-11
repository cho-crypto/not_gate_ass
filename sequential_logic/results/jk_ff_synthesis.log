library ieee;
use ieee.std_logic_1164.all;
entity jk_ff is
  port (
    j: in std_logic;
    k: in std_logic;
    clk: in std_logic;
    clr_n: in std_logic;
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
  signal wrap_clr_n: std_logic;
  signal wrap_q: std_logic;
  signal wrap_qb: std_logic;
  signal q_i : std_logic;
  signal n4 : std_logic;
  signal n6 : std_logic;
  signal n7 : std_logic;
  signal n8 : std_logic;
  signal n9 : std_logic;
  signal n10 : std_logic;
  signal n11 : std_logic;
  signal n12 : std_logic;
  signal n14 : std_logic;
  signal n16 : std_logic;
  signal n21 : std_logic;
  signal n22 : std_logic;
begin
  wrap_j <= j;
  wrap_k <= k;
  wrap_clk <= clk;
  wrap_clr_n <= clr_n;
  q <= wrap_q;
  qb <= wrap_qb;
  wrap_q <= q_i;
  wrap_qb <= n21;
  -- vhdl/jk_ff.vhd:15:10
  q_i <= n22; -- (signal)
  -- vhdl/jk_ff.vhd:20:14
  n4 <= not wrap_clr_n;
  -- vhdl/jk_ff.vhd:22:12
  n6 <= not wrap_j;
  -- vhdl/jk_ff.vhd:22:18
  n7 <= wrap_k and n6;
  -- vhdl/jk_ff.vhd:23:27
  n8 <= not wrap_k;
  -- vhdl/jk_ff.vhd:23:21
  n9 <= n8 and wrap_j;
  -- vhdl/jk_ff.vhd:24:21
  n10 <= wrap_k and wrap_j;
  -- vhdl/jk_ff.vhd:24:45
  n11 <= not q_i;
  -- vhdl/jk_ff.vhd:24:7
  n12 <= q_i when n10 = '0' else n11;
  -- vhdl/jk_ff.vhd:23:7
  n14 <= n12 when n9 = '0' else '1';
  -- vhdl/jk_ff.vhd:22:7
  n16 <= n14 when n7 = '0' else '0';
  -- vhdl/jk_ff.vhd:28:19
  n21 <= not q_i;
  -- vhdl/jk_ff.vhd:21:5
  process (wrap_clk, n4)
  begin
    if n4 = '1' then
      n22 <= '0';
    elsif rising_edge (wrap_clk) then
      n22 <= n16;
    end if;
  end process;
end rtl;
