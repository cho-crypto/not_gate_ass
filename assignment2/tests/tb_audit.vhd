-- Independent review: expectations use named illuminated segments instead
-- of copying the implementation's binary lookup constants.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity tb_audit is end;
architecture test of tb_audit is
  signal sel : std_logic_vector(2 downto 0) := (others=>'0');
  signal n : std_logic_vector(3 downto 0) := (others=>'0');
  signal vt : std_logic_vector(12 downto 0) := (others=>'0');
  signal votes : std_logic_vector(24 downto 0) := (others=>'0');
  signal en, result, y : std_logic := '0';
  signal md : std_logic_vector(7 downto 0) := (others=>'0');
  signal ms : std_logic_vector(2 downto 0) := (others=>'0');
  signal glyph, counted, hexadecimal : std_logic_vector(7 downto 0);

  function lit(names : string) return std_logic_vector is
    variable v : std_logic_vector(7 downto 0) := (others=>'0');
  begin
    for i in names'range loop
      v(7-(character'pos(names(i))-character'pos('a'))) := '1';
    end loop;
    return v;
  end;
  function hex_expected(i : natural) return std_logic_vector is
  begin
    case i is
      when 0 => return lit("abcdef");
      when 1 => return lit("bc");
      when 2 => return lit("abdeg");
      when 3 => return lit("abcdg");
      when 4 => return lit("bcfg");
      when 5 => return lit("acdfg");
      when 6 => return lit("acdefg");
      when 7 => return lit("abc");
      when 8 => return lit("abcdefg");
      when 9 => return lit("abcdfg");
      when 10 => return lit("abcefg");
      when 11 => return lit("cdefg");
      when 12 => return lit("adef");
      when 13 => return lit("bcdeg");
      when 14 => return lit("adefg");
      when 15 => return lit("aefg");
      when others => return lit("");
    end case;
  end;
  function count_expected(i : natural) return natural is
    variable value : natural := i;
    variable count : natural := 0;
  begin
    while value /= 0 loop
      count := count + value mod 2;
      value := value/2;
    end loop;
    return count;
  end;
begin
  u1 : entity work.letters7seg port map(sel,glyph);
  u2 : entity work.hex7seg port map(n,hexadecimal);
  u3 : entity work.popcount13_display port map(vt,en,counted);
  u4 : entity work.voting25 port map(votes,result);
  u5 : entity work.mux8 port map(md,ms,y);
  check : process
    variable expected : std_logic_vector(7 downto 0);
  begin
    for i in 0 to 15 loop
      n <= std_logic_vector(to_unsigned(i,4)); wait for 10 ns;
      assert hexadecimal=hex_expected(i) report "AUDIT HEX segment mismatch" severity failure;
    end loop;
    report "AUDIT PASS: 16 hexadecimal glyphs, independent named-segment reference";
    for i in 0 to 7 loop
      case i is
        when 0 => expected:=lit("abcefg");
        when 1 => expected:=lit("cdefg");
        when 2 => expected:=lit("adef");
        when 3 => expected:=lit("bcdeg");
        when 4 => expected:=lit("aefg");
        when 5 => expected:=lit("acdefg");
        when others => expected:=lit("");
      end case;
      sel <= std_logic_vector(to_unsigned(i,3)); wait for 10 ns;
      assert glyph=expected report "AUDIT LETTER segment mismatch" severity failure;
    end loop;
    report "AUDIT PASS: 8 letter selectors, independent named-segment reference";
    for i in 0 to 8191 loop
      vt<=std_logic_vector(to_unsigned(i,13));
      en<='1'; wait for 10 ns;
      assert counted=hex_expected(count_expected(i)) report "AUDIT COUNT enabled mismatch" severity failure;
      en<='0'; wait for 10 ns;
      assert counted=lit("") report "AUDIT COUNT disable mismatch" severity failure;
    end loop;
    report "AUDIT PASS: 16384 vt/enable combinations, independent segment reference";
    -- Defensive checks beyond the assignment's stable binary-input scope.
    vt <= (others=>'X'); en<='0'; wait for 10 ns;
    assert counted=lit("") report "AUDIT disable must dominate unknown vt" severity failure;
    en<='1'; wait for 10 ns;
    assert counted=(counted'range=>'X') report "AUDIT unknown vt must be flagged" severity failure;
    vt <= (others=>'0'); en<='X'; wait for 10 ns;
    assert counted=(counted'range=>'X') report "AUDIT unknown enable must be flagged" severity failure;
    votes <= (others=>'X'); ms <= "XXX"; wait for 10 ns;
    assert result='X' report "AUDIT unknown vote must be flagged" severity failure;
    assert y='X' report "AUDIT unknown select must be flagged" severity failure;
    report "AUDIT PASS: 5 nonbinary/disable assertions";
    report "ALL INDEPENDENT AUDIT TESTS PASSED";
    std.env.finish;
    wait;
  end process;
end test;
