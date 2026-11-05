library ieee;
use ieee.std_logic_1164.all;

entity d_latch_gates is
  port (d : in std_logic; en : in std_logic; q, qb : out std_logic);
end entity;

architecture gates of d_latch_gates is
  signal dn, sb, rb : std_logic;
begin
  dn <= not (d and d) after 1 ns;
  sb <= not (d and en) after 1 ns;
  rb <= not (dn and en) after 1 ns;
  q <= not (sb and qb) after 1 ns;
  qb <= not (rb and q) after 1 ns;
end architecture;
