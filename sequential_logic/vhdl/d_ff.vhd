library ieee;
use ieee.std_logic_1164.all;

entity d_ff is
  port (
    d : in std_logic;
    clk : in std_logic;
    q, qb : out std_logic
  );
end entity;

architecture rtl of d_ff is
  signal q_i : std_logic;
begin
  process(clk)
  begin
    if rising_edge(clk) then q_i <= d; end if;
  end process;
  q <= q_i; qb <= not q_i;
end architecture;
