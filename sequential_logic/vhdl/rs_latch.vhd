library ieee;
use ieee.std_logic_1164.all;

entity rs_latch is
  port (
    s : in std_logic;
    r : in std_logic;
    q, qb : out std_logic
  );
end entity;

architecture rtl of rs_latch is
  signal q_i, qb_i : std_logic;
begin
  -- Active-high NOR latch. s=r=1 forces q=qb=0 (forbidden).
  -- Releasing both controls simultaneously is not a valid state recovery.
  q_i <= not (r or qb_i);
  qb_i <= not (s or q_i);
  q <= q_i; qb <= qb_i;
end architecture;
