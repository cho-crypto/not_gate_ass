library ieee;
use ieee.std_logic_1164.all;

entity d_ff_async is
  port (
    d : in std_logic;
    clk : in std_logic;
    set : in std_logic;
    clr : in std_logic;
    q, qb : out std_logic
  );
end entity;

architecture rtl of d_ff_async is
  signal q_i : std_logic;
begin
  process(clk, set, clr)
  begin
    if clr = '1' then q_i <= '0';
    elsif set = '1' then q_i <= '1';
    elsif rising_edge(clk) then q_i <= d;
    end if;
  end process;
  q <= q_i; qb <= not q_i;
end architecture;
