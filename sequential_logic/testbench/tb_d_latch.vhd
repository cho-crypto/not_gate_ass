library ieee;
use ieee.std_logic_1164.all;

use std.env.all;

entity tb_d_latch is end;
architecture test of tb_d_latch is
  signal d, en : std_logic := '0';
  signal q, qb, gq, gqb : std_logic;
begin
  dut: entity work.d_latch(rtl) port map(d, en, q, qb);
  net: entity work.d_latch_gates(gates) port map(d, en, gq, gqb);
  process
  begin
    d <= '0'; en <= '1';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 1: Initialize transparent" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 1: Initialize transparent" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 1" severity failure;
    report "PASS step 1: Initialize transparent" severity note;
    d <= '1'; en <= '1';
    wait for 30 ns;
    assert q = '1' and qb = '0' report "RTL step 2: Follow 1" severity failure;
    assert gq = '1' and gqb = '0' report "Gates step 2: Follow 1" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 2" severity failure;
    report "PASS step 2: Follow 1" severity note;
    d <= '1'; en <= '0';
    wait for 30 ns;
    assert q = '1' and qb = '0' report "RTL step 3: Close latch" severity failure;
    assert gq = '1' and gqb = '0' report "Gates step 3: Close latch" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 3" severity failure;
    report "PASS step 3: Close latch" severity note;
    d <= '0'; en <= '0';
    wait for 30 ns;
    assert q = '1' and qb = '0' report "RTL step 4: Hold despite D change" severity failure;
    assert gq = '1' and gqb = '0' report "Gates step 4: Hold despite D change" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 4" severity failure;
    report "PASS step 4: Hold despite D change" severity note;
    d <= '0'; en <= '1';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 5: Follow 0" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 5: Follow 0" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 5" severity failure;
    report "PASS step 5: Follow 0" severity note;
    d <= '0'; en <= '0';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 6: Close at 0" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 6: Close at 0" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 6" severity failure;
    report "PASS step 6: Close at 0" severity note;
    d <= '1'; en <= '0';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 7: Hold 0" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 7: Hold 0" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 7" severity failure;
    report "PASS step 7: Hold 0" severity note;
    d <= '1'; en <= '1';
    wait for 30 ns;
    assert q = '1' and qb = '0' report "RTL step 8: Follow again" severity failure;
    assert gq = '1' and gqb = '0' report "Gates step 8: Follow again" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 8" severity failure;
    report "PASS step 8: Follow again" severity note;
    report "ALL PASS d_latch" severity note;
    finish;
    wait;
  end process;
end architecture;
