library ieee;
use ieee.std_logic_1164.all;
entity d_ff_async is
  port (
    d: in std_logic;
    clk: in std_logic;
    set: in std_logic;
    clr: in std_logic;
    q, qb: out std_logic
  );
end entity;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

architecture rtl of d_ff_async is
  signal wrap_d: std_logic;
  signal wrap_clk: std_logic;
  signal wrap_set: std_logic;
  signal wrap_clr: std_logic;
  signal wrap_q: std_logic;
  signal wrap_qb: std_logic;
  signal q_i : std_logic;
  signal n7 : std_logic;
  signal n11 : std_logic;
  signal n12 : std_logic;
  signal n13 : std_logic;
begin
  wrap_d <= d;
  wrap_clk <= clk;
  wrap_set <= set;
  wrap_clr <= clr;
  q <= wrap_q;
  qb <= wrap_qb;
  wrap_q <= q_i;
  wrap_qb <= n11;
  -- vhdl/d_ff_async.vhd:15:10
  q_i <= n13; -- (signal)
  -- vhdl/d_ff_async.vhd:20:5
  n7 <= '1' when wrap_clr = '0' else '0';
  -- vhdl/d_ff_async.vhd:24:19
  n11 <= not q_i;
  -- vhdl/d_ff_async.vhd:4:8
  n12 <= wrap_clr or wrap_set;
  -- vhdl/d_ff_async.vhd:21:5
  process (wrap_clk, n12, n7)
  begin
    if n12 = '1' then
      n13 <= n7;
    elsif rising_edge (wrap_clk) then
      n13 <= wrap_d;
    end if;
  end process;
end rtl;
