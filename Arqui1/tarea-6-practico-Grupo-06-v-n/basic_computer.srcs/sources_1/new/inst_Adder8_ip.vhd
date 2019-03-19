
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Adder8_ip is
    Port ( d_in : in STD_LOGIC_VECTOR (7 downto 0);
           s : out STD_LOGIC_VECTOR (7 downto 0));
end Adder8_ip;

architecture Behavioral of Adder8_ip is
component Adder8 
    Port ( a : in STD_LOGIC_VECTOR (7 downto 0);
           b : in STD_LOGIC_VECTOR (7 downto 0);
           ci : in STD_LOGIC;
           s : out STD_LOGIC_VECTOR (7 downto 0);
           co : out STD_LOGIC);
    end component;

signal a1: std_logic_vector(7 downto 0); 
signal b3: std_logic_vector(7 downto 0); 
signal a5: std_logic_vector(7 downto 0); 
signal b7: std_logic_vector(7 downto 0);
signal s2: std_logic_vector(7 downto 0); 
signal s3: std_logic_vector(7 downto 0); 
signal co: std_logic_vector(2 downto 0); 

begin

a1 <= "0000000" & d_in(1);
b3 <= "0000000" & d_in(3); 
a5 <= "0000000" & d_in(5); 
b7 <= "0000000" & d_in(7);
 
inst_Adder8_0: Adder8 port map(
        a      =>a1,
        b      =>b3,
        ci     => '0',
        s      =>s2,
        co     => co(0) 
        );

inst_Adder8_1: Adder8 port map(
        a      =>a5,
        b      =>b7,
        ci     => '0',
        s      =>s3,
        co     => co(1)
    );
    
inst_Adder8_2: Adder8 port map( 
            a      =>s2, 
            b      =>s3,
            ci     =>'0',
            s      =>s,
            co     =>co(2)
        ); 

end Behavioral;
