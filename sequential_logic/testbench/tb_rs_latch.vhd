library ieee;
use ieee.std_logic_1164.all;

use std.env.all;

entity tb_rs_latch is end;
architecture test of tb_rs_latch is
  signal s, r : std_logic := '0';
  signal q, qb, gq, gqb : std_logic;
begin
  dut: entity work.rs_latch(rtl) port map(s, r, q, qb);
  net: entity work.rs_latch_gates(gates) port map(s, r, gq, gqb);
  process
  begin
    s <= '0'; r <= '1';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 1: Reset" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 1: Reset" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 1" severity failure;
    report "PASS step 1: Reset" severity note;
    s <= '0'; r <= '0';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 2: Hold 0" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 2: Hold 0" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 2" severity failure;
    report "PASS step 2: Hold 0" severity note;
    s <= '1'; r <= '0';
    wait for 30 ns;
    assert q = '1' and qb = '0' report "RTL step 3: Set" severity failure;
    assert gq = '1' and gqb = '0' report "Gates step 3: Set" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 3" severity failure;
    report "PASS step 3: Set" severity note;
    s <= '0'; r <= '0';
    wait for 30 ns;
    assert q = '1' and qb = '0' report "RTL step 4: Hold 1" severity failure;
    assert gq = '1' and gqb = '0' report "Gates step 4: Hold 1" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 4" severity failure;
    report "PASS step 4: Hold 1" severity note;
    s <= '1'; r <= '1';
    wait for 30 ns;
    assert q = '0' and qb = '0' report "RTL step 5: Forbidden" severity failure;
    assert gq = '0' and gqb = '0' report "Gates step 5: Forbidden" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 5" severity failure;
    report "PASS step 5: Forbidden" severity note;
    s <= '0'; r <= '1';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 6: Recover via Reset" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 6: Recover via Reset" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 6" severity failure;
    report "PASS step 6: Recover via Reset" severity note;
    s <= '0'; r <= '0';
    wait for 30 ns;
    assert q = '0' and qb = '1' report "RTL step 7: Hold after recovery" severity failure;
    assert gq = '0' and gqb = '1' report "Gates step 7: Hold after recovery" severity failure;
    assert q = gq and qb = gqb report "Equivalence step 7" severity failure;
    report "PASS step 7: Hold after recovery" severity note;
    report "ALL PASS rs_latch" severity note;
    finish;
    wait;
  end process;
end architecture;
