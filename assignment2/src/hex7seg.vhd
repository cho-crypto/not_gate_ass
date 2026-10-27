library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity hex7seg is
  port (n : in std_logic_vector(3 downto 0);
        seg : out std_logic_vector(7 downto 0));
end hex7seg;

architecture rtl of hex7seg is
begin
  -- seg = abcdefg dp, active high.
  with n select seg <=
    "11111100" when "0000",
    "01100000" when "0001",
    "11011010" when "0010",
    "11110010" when "0011",
    "01100110" when "0100",
    "10110110" when "0101",
    "10111110" when "0110",
    "11100000" when "0111",
    "11111110" when "1000",
    "11110110" when "1001",
    "11101110" when "1010",
    "00111110" when "1011",
    "10011100" when "1100",
    "01111010" when "1101",
    "10011110" when "1110",
    "10001110" when "1111",
    (others => 'X') when others;
end rtl;
