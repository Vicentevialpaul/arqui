library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity AddSu8 is
    Port ( a    : in  std_logic_vector (7 downto 0);
           b    : in  std_logic_vector (7 downto 0);
           ci   : in  std_logic;
           sub  : in  std_logic;
           co   : out std_logic;
           s    : out std_logic_vector (7 downto 0));
end AddSu8;

architecture Behavioral of AddSu8 is

component Adder8 
    Port ( a    : in  std_logic_vector (7 downto 0);
           b    : in  std_logic_vector (7 downto 0);
           ci   : in  std_logic;
           s    : out std_logic_vector (7 downto 0);
           co   : out std_logic);
    end component;

signal alt_b : std_logic_vector(7 downto 0);

begin

with sub select
     alt_b <=  b when '0',
               not b when '1',
               b when others; 

inst_Adder8: Adder8 port map(
        a      =>a,
        b      =>alt_b,
        ci     =>ci,
        s      =>s,
        co     =>co
    );

end Behavioral;
