library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity letters7seg is
  port (sel : in std_logic_vector(2 downto 0);
        seg : out std_logic_vector(7 downto 0));
end letters7seg;

architecture rtl of letters7seg is
begin
  -- seg(7 downto 0) = a,b,c,d,e,f,g,dp; 1 turns a segment on.
  -- 000..101: a,b,c,d,f,g (A,b,C,d,F,G on seven segments).
  with sel select seg <=
    "11101110" when "000",
    "00111110" when "001",
    "10011100" when "010",
    "01111010" when "011",
    "10001110" when "100",
    "10111110" when "101",
    "00000000" when others;
end rtl;
