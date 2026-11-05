library ieee;
use ieee.std_logic_1164.all;

entity jk_ff_gates is
  port (j : in std_logic; k : in std_logic; clk : in std_logic; q, qb : out std_logic);
end entity;

architecture gates of jk_ff_gates is
  signal clkn, kn, jterm, kterm, next_d, m_dn, m_sb, m_rb, mq, mqb, s_dn, s_sb, s_rb : std_logic;
begin
  clkn <= not (clk and clk) after 1 ns;
  kn <= not (k and k) after 1 ns;
  jterm <= not (j and qb) after 1 ns;
  kterm <= not (kn and q) after 1 ns;
  next_d <= not (jterm and kterm) after 1 ns;
  m_dn <= not (next_d and next_d) after 1 ns;
  m_sb <= not (next_d and clkn) after 1 ns;
  m_rb <= not (m_dn and clkn) after 1 ns;
  mq <= not (m_sb and mqb) after 1 ns;
  mqb <= not (m_rb and mq) after 1 ns;
  s_dn <= not (mq and mq) after 1 ns;
  s_sb <= not (mq and clk) after 1 ns;
  s_rb <= not (s_dn and clk) after 1 ns;
  q <= not (s_sb and qb) after 1 ns;
  qb <= not (s_rb and q) after 1 ns;
end architecture;
