
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Adder8_p is
    Port ( d_in : in STD_LOGIC_VECTOR (7 downto 0);
           s : out STD_LOGIC_VECTOR (7 downto 0));
end Adder8_p;

architecture Behavioral of Adder8_p is
component Adder8 
    Port ( a : in STD_LOGIC_VECTOR (7 downto 0);
           b : in STD_LOGIC_VECTOR (7 downto 0);
           ci : in STD_LOGIC;
           s : out STD_LOGIC_VECTOR (7 downto 0);
           co : out STD_LOGIC);
    end component;

signal a0: std_logic_vector(7 downto 0); 
signal b2: std_logic_vector(7 downto 0); 
signal a4: std_logic_vector(7 downto 0); 
signal b6: std_logic_vector(7 downto 0);
signal s0: std_logic_vector(7 downto 0); 
signal s1: std_logic_vector(7 downto 0); 
signal co: std_logic_vector(2 downto 0); 

begin

a0 <= "0000000" & d_in(0);
b2 <= "0000000" & d_in(2); 
a4 <= "0000000" & d_in(4); 
b6 <= "0000000" & d_in(6);
 
inst_Adder8_0: Adder8 port map(
        a      =>a0,
        b      =>b2,
        ci     => '0',
        s      =>s0,
        co     => co(0) 
        );

inst_Adder8_1: Adder8 port map(
        a      =>a4,
        b      =>b6,
        ci     => '0',
        s      =>s1, 
        co     => co(1)
    );

inst_Adder8_2: Adder8 port map( 
        a      =>s0, 
        b      =>s1,
        ci     =>'0',
        s      =>s,
        co     =>co(2)
    ); 

end Behavioral;
