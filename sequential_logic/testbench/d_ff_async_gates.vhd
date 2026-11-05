library ieee;
use ieee.std_logic_1164.all;

entity d_ff_async_gates is
  port (d : in std_logic; clk : in std_logic; set : in std_logic; clr : in std_logic; q, qb : out std_logic);
end entity;

architecture gates of d_ff_async_gates is
  signal clkn, clrn, setn, idle_n, idle, men_n, men, sen_n, sen, m_dn, m_sb, m_rb, m_qsn, m_qsab, mq, m_qrn, m_qrab, mqb, s_dn, s_sb, s_rb, s_qsn, s_qsab, s_qrn, s_qrab : std_logic;
begin
  clkn <= not (clk and clk) after 1 ns;
  clrn <= not (clr and clr) after 1 ns;
  setn <= not (set and clrn) after 1 ns;
  idle_n <= not (clrn and setn) after 1 ns;
  idle <= not (idle_n and idle_n) after 1 ns;
  men_n <= not (clkn and idle) after 1 ns;
  men <= not (men_n and men_n) after 1 ns;
  sen_n <= not (clk and idle) after 1 ns;
  sen <= not (sen_n and sen_n) after 1 ns;
  m_dn <= not (d and d) after 1 ns;
  m_sb <= not (d and men) after 1 ns;
  m_rb <= not (m_dn and men) after 1 ns;
  m_qsn <= not (m_sb and mqb) after 1 ns;
  m_qsab <= not (m_qsn and m_qsn) after 1 ns;
  mq <= not (m_qsab and setn) after 1 ns;
  m_qrn <= not (m_rb and mq) after 1 ns;
  m_qrab <= not (m_qrn and m_qrn) after 1 ns;
  mqb <= not (m_qrab and clrn) after 1 ns;
  s_dn <= not (mq and mq) after 1 ns;
  s_sb <= not (mq and sen) after 1 ns;
  s_rb <= not (s_dn and sen) after 1 ns;
  s_qsn <= not (s_sb and qb) after 1 ns;
  s_qsab <= not (s_qsn and s_qsn) after 1 ns;
  q <= not (s_qsab and setn) after 1 ns;
  s_qrn <= not (s_rb and q) after 1 ns;
  s_qrab <= not (s_qrn and s_qrn) after 1 ns;
  qb <= not (s_qrab and clrn) after 1 ns;
end architecture;
