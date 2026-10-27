library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity mux8 is
  port (d : in std_logic_vector(7 downto 0);
        s : in std_logic_vector(2 downto 0);
        y : out std_logic);
end mux8;

architecture rtl of mux8 is
begin
  -- s=000 selects d(0), s=111 selects d(7).
  with s select y <=
    d(0) when "000", d(1) when "001",
    d(2) when "010", d(3) when "011",
    d(4) when "100", d(5) when "101",
    d(6) when "110", d(7) when "111",
    'X' when others;
end rtl;
