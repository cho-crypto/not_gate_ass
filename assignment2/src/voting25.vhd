library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity voting25 is
  port (vt : in std_logic_vector(24 downto 0);
        result : out std_logic);
end voting25;

architecture rtl of voting25 is
begin
  process(vt)
    variable count : integer range 0 to 25;
    variable valid : boolean;
  begin
    count := 0;
    valid := true;
    for i in vt'range loop
      if vt(i) = '1' then count := count + 1;
      elsif vt(i) /= '0' then valid := false;
      end if;
    end loop;
    if not valid then result <= 'X';
    elsif count >= 13 then result <= '1';
    else result <= '0';
    end if;
  end process;
end rtl;
