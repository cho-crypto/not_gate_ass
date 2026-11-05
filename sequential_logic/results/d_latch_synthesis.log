library ieee;
use ieee.std_logic_1164.all;
entity d_latch is
  port (
    d: in std_logic;
    en: in std_logic;
    q, qb: out std_logic
  );
end entity;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

architecture rtl of d_latch is
  signal wrap_d: std_logic;
  signal wrap_en: std_logic;
  signal wrap_q: std_logic;
  signal wrap_qb: std_logic;
  signal q_i : std_logic;
  signal n6 : std_logic;
  signal n7 : std_logic;
begin
  wrap_d <= d;
  wrap_en <= en;
  q <= wrap_q;
  qb <= wrap_qb;
  wrap_q <= q_i;
  wrap_qb <= n6;
  -- vhdl/d_latch.vhd:13:10
  q_i <= n7; -- (signal)
  -- vhdl/d_latch.vhd:19:19
  n6 <= not q_i;
  -- vhdl/d_latch.vhd:13:10
  n7 <= wrap_d when wrap_en = '1' else n7;
end rtl;
