library ieee;
use ieee.std_logic_1164.all;

entity rs_latch_gates is
  port (s : in std_logic; r : in std_logic; q, qb : out std_logic);
end entity;

architecture gates of rs_latch_gates is
begin
  q <= not (r or qb) after 1 ns;
  qb <= not (s or q) after 1 ns;
end architecture;
