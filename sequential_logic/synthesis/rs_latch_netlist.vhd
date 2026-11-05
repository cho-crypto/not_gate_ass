library ieee;
use ieee.std_logic_1164.all;
entity rs_latch is
  port (
    s: in std_logic;
    r: in std_logic;
    q, qb: out std_logic
  );
end entity;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

architecture rtl of rs_latch is
  signal wrap_s: std_logic;
  signal wrap_r: std_logic;
  signal wrap_q: std_logic;
  signal wrap_qb: std_logic;
  signal q_i : std_logic;
  signal qb_i : std_logic;
  signal n2 : std_logic;
  signal n3 : std_logic;
  signal n4 : std_logic;
  signal n5 : std_logic;
begin
  wrap_s <= s;
  wrap_r <= r;
  q <= wrap_q;
  qb <= wrap_qb;
  wrap_q <= q_i;
  wrap_qb <= qb_i;
  -- vhdl/rs_latch.vhd:13:10
  q_i <= n3; -- (signal)
  -- vhdl/rs_latch.vhd:13:15
  qb_i <= n5; -- (signal)
  -- vhdl/rs_latch.vhd:17:17
  n2 <= wrap_r or qb_i;
  -- vhdl/rs_latch.vhd:17:10
  n3 <= not n2;
  -- vhdl/rs_latch.vhd:18:18
  n4 <= wrap_s or q_i;
  -- vhdl/rs_latch.vhd:18:11
  n5 <= not n4;
end rtl;
