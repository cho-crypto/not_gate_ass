library ieee;
use ieee.std_logic_1164.all;

entity jk_ff is
  port (
    j : in std_logic;
    k : in std_logic;
    clk : in std_logic;
    clr_n : in std_logic;
    q, qb : out std_logic
  );
end entity;

architecture rtl of jk_ff is
  signal q_i : std_logic;
begin
  -- Active-low asynchronous Clear, common to master and slave.
  process(clk, clr_n)
  begin
    if clr_n = '0' then q_i <= '0';
    elsif rising_edge(clk) then
      if j = '0' and k = '1' then q_i <= '0';
      elsif j = '1' and k = '0' then q_i <= '1';
      elsif j = '1' and k = '1' then q_i <= not q_i;
      end if;
    end if;
  end process;
  q <= q_i; qb <= not q_i;
end architecture;
