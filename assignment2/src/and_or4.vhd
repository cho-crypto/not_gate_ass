library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity and_or4 is
  port (a, b, c, d : in std_logic;
        out1, out2 : out std_logic);
end and_or4;

architecture rtl of and_or4 is
begin
  out1 <= a and b and c and d;
  out2 <= a or b or c or d;
end rtl;
