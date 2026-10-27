library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

use std.textio.all;
entity tb_assignment2 is end;
architecture test of tb_assignment2 is
  signal a,b,c,d,out1,out2,my : std_logic := '0';
  signal md : std_logic_vector(7 downto 0) := (others=>'0');
  signal ms,ls : std_logic_vector(2 downto 0) := (others=>'0');
  signal lseg,pseg,hseg : std_logic_vector(7 downto 0);
  signal v25 : std_logic_vector(24 downto 0) := (others=>'0');
  signal vr,en : std_logic := '0';
  signal v13 : std_logic_vector(12 downto 0) := (others=>'0');
  signal hn : std_logic_vector(3 downto 0) := (others=>'0');
  type patterns is array(natural range <>) of std_logic_vector(7 downto 0);
  constant hx : patterns(0 to 15) := ("11111100","01100000","11011010","11110010","01100110","10110110","10111110","11100000","11111110","11110110","11101110","00111110","10011100","01111010","10011110","10001110");
  constant lt : patterns(0 to 7) := ("11101110","00111110","10011100","01111010","10001110","10111110","00000000","00000000");
  function ones(n : natural; width : positive) return natural is
    variable x : natural := n;
    variable total : natural := 0;
  begin
    for i in 1 to width loop total:=total+(x mod 2); x:=x/2; end loop;
    return total;
  end;
  function logic(b : boolean) return std_logic is
  begin
    if b then return '1'; else return '0'; end if;
  end;
begin
  u1: entity work.and_or4 port map(a,b,c,d,out1,out2);
  u2: entity work.mux8 port map(md,ms,my);
  u3: entity work.letters7seg port map(ls,lseg);
  u4: entity work.voting25 port map(v25,vr);
  u5: entity work.popcount13_display port map(v13,en,pseg);
  u6: entity work.hex7seg port map(hn,hseg);
  stimulus: process
    variable q: std_logic_vector(3 downto 0);
    file vf : text open read_mode is "tests/voting25_vectors.txt";
    variable line_in: line;
    variable n, tested: integer := 0;
  begin
    for i in 0 to 15 loop
      q:=std_logic_vector(to_unsigned(i,4)); a<=q(3);b<=q(2);c<=q(1);d<=q(0);
      wait for 10 ns;
      assert out1=logic(i=15) report "Q1 AND mismatch" severity failure;
      assert out2=logic(i/=0) report "Q1 OR mismatch" severity failure;
    end loop;
    report "PASS Q1: 16 exhaustive input combinations";
    for i in 0 to 255 loop
      md<=std_logic_vector(to_unsigned(i,8));
      for j in 0 to 7 loop
        ms<=std_logic_vector(to_unsigned(j,3)); wait for 10 ns;
        assert my=md(j) report "Q2 mux mismatch" severity failure;
      end loop;
    end loop;
    report "PASS Q2: 2048 exhaustive data/select combinations";
    for i in 0 to 7 loop
      ls<=std_logic_vector(to_unsigned(i,3)); wait for 10 ns;
      assert lseg=lt(i) report "Q3 glyph mismatch" severity failure;
    end loop;
    report "PASS Q3: 8 selectors, including 2 blank codes";
    while not endfile(vf) loop
      readline(vf,line_in);read(line_in,n);v25<=std_logic_vector(to_unsigned(n,25));
      wait for 10 ns;
      assert vr=logic(ones(n,25)>=13) report "Q4 majority mismatch" severity failure;
      tested:=tested+1;
    end loop;
    report "PASS Q4: " & integer'image(tested) & " deterministic vectors (all counts, rotated boundaries, random)";
    for i in 0 to 8191 loop
      v13<=std_logic_vector(to_unsigned(i,13));
      en<='0'; wait for 10 ns;
      assert pseg="00000000" report "Q5 disable mismatch" severity failure;
      en<='1'; wait for 10 ns;
      assert pseg=hx(ones(i,13)) report "Q5 population/display mismatch" severity failure;
    end loop;
    report "PASS Q5: 16384 exhaustive vt/enable combinations";
    for i in 0 to 15 loop
      hn<=std_logic_vector(to_unsigned(i,4)); wait for 10 ns;
      assert hseg=hx(i) report "HEX decoder mismatch" severity failure;
    end loop;
    report "PASS HEX: all 16 symbols (including unreachable E,F for Q5)";
    report "ALL TESTS PASSED";
    std.env.finish;
    wait;
  end process;
end test;
