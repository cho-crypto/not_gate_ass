library ieee;
use ieee.std_logic_1164.all;
entity d_ff is
  port (
    d: in std_logic;
    clk: in std_logic;
    q, qb: out std_logic
  );
end entity;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

architecture rtl of d_ff is
  signal wrap_d: std_logic;
  signal wrap_clk: std_logic;
  signal wrap_q: std_logic;
  signal wrap_qb: std_logic;
  signal q_i : std_logic;
  signal n7 : std_logic;
  signal n8 : std_logic;
begin
  wrap_d <= d;
  wrap_clk <= clk;
  q <= wrap_q;
  qb <= wrap_qb;
  wrap_q <= q_i;
  wrap_qb <= n7;
  -- vhdl/d_ff.vhd:13:10
  q_i <= n8; -- (signal)
  -- vhdl/d_ff.vhd:19:19
  n7 <= not q_i;
  -- vhdl/d_ff.vhd:17:5
  process (wrap_clk)
  begin
    if rising_edge (wrap_clk) then
      n8 <= wrap_d;
    end if;
  end process;
end rtl;
