library ieee;
use ieee.std_logic_1164.all;

entity jk_ff_gates is
  port (j : in std_logic; k : in std_logic; clk : in std_logic; clr_n : in std_logic; q, qb : out std_logic);
end entity;

architecture gates of jk_ff_gates is
  signal clkn, kn, jterm, kterm, next_d, men_n, men, sen_n, sen, m_dn, m_sb, m_rb, mq, m_clear_n, m_clear_ab, mqb, s_dn, s_sb, s_rb, s_clear_n, s_clear_ab : std_logic;
begin
  clkn <= not (clk and clk) after 1 ns;
  kn <= not (k and k) after 1 ns;
  jterm <= not (j and qb) after 1 ns;
  kterm <= not (kn and q) after 1 ns;
  next_d <= not (jterm and kterm) after 1 ns;
  men_n <= not (clkn and clr_n) after 1 ns;
  men <= not (men_n and men_n) after 1 ns;
  sen_n <= not (clk and clr_n) after 1 ns;
  sen <= not (sen_n and sen_n) after 1 ns;
  m_dn <= not (next_d and next_d) after 1 ns;
  m_sb <= not (next_d and men) after 1 ns;
  m_rb <= not (m_dn and men) after 1 ns;
  mq <= not (m_sb and mqb) after 1 ns;
  m_clear_n <= not (m_rb and mq) after 1 ns;
  m_clear_ab <= not (m_clear_n and m_clear_n) after 1 ns;
  mqb <= not (m_clear_ab and clr_n) after 1 ns;
  s_dn <= not (mq and mq) after 1 ns;
  s_sb <= not (mq and sen) after 1 ns;
  s_rb <= not (s_dn and sen) after 1 ns;
  q <= not (s_sb and qb) after 1 ns;
  s_clear_n <= not (s_rb and q) after 1 ns;
  s_clear_ab <= not (s_clear_n and s_clear_n) after 1 ns;
  qb <= not (s_clear_ab and clr_n) after 1 ns;
end architecture;
