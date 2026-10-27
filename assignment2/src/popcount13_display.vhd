library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity popcount13_display is
  port (vt : in std_logic_vector(12 downto 0);
        en : in std_logic;
        seg : out std_logic_vector(7 downto 0));
end popcount13_display;

architecture rtl of popcount13_display is
begin
  process(vt, en)
    variable count : integer range 0 to 13;
    variable valid : boolean;
  begin
    count := 0;
    valid := true;
    for i in vt'range loop
      if vt(i) = '1' then count := count + 1;
      elsif vt(i) /= '0' then valid := false;
      end if;
    end loop;
    if en = '0' then seg <= "00000000";
    elsif en /= '1' or not valid then seg <= (others => 'X');
    else
      case count is
        when 0 => seg <= "11111100";
        when 1 => seg <= "01100000";
        when 2 => seg <= "11011010";
        when 3 => seg <= "11110010";
        when 4 => seg <= "01100110";
        when 5 => seg <= "10110110";
        when 6 => seg <= "10111110";
        when 7 => seg <= "11100000";
        when 8 => seg <= "11111110";
        when 9 => seg <= "11110110";
        when 10 => seg <= "11101110";
        when 11 => seg <= "00111110";
        when 12 => seg <= "10011100";
        when 13 => seg <= "01111010";
        -- E and F are defined for a reusable hexadecimal decoder;
        -- 14 and 15 are unreachable with a 13-bit input.
        when others => seg <= "00000000";
      end case;
    end if;
  end process;
end rtl;
