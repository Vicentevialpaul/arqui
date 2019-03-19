
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


entity Sub_ip_p is
    Port ( data_in : in STD_LOGIC_VECTOR (7 downto 0);
           s : out STD_LOGIC_VECTOR (7 downto 0));
end Sub_ip_p;

architecture Behavioral of Sub_ip_p is

component AddSu8
    Port ( a    : in  std_logic_vector (7 downto 0);
           b    : in  std_logic_vector (7 downto 0);
           ci   : in  std_logic;
           sub  : in  std_logic;
           co   : out std_logic;
           s    : out std_logic_vector (7 downto 0));
    end component;
    
component Adder8_ip
    Port ( d_in : in STD_LOGIC_VECTOR (7 downto 0);
           s : out STD_LOGIC_VECTOR (7 downto 0));
    end component; 

component Adder8_p
    Port ( d_in : in STD_LOGIC_VECTOR (7 downto 0);
           s : out STD_LOGIC_VECTOR (7 downto 0));
    end component; 

signal z0: std_logic_vector(7 downto 0);
signal z1: std_logic_vector(7 downto 0); 
signal co: std_logic; 


begin
inst_Adder_ip: Adder8_ip port map( 
    d_in     =>data_in,
    s        =>z0
    ); 
    
inst_Adder_p: Adder8_p port map(     
    d_in      =>data_in, 
    s         =>z1
    ); 
    
inst_AddSu8: AddSu8 port map( 
    a       =>z0, 
    b       =>z1,
    ci      => '1', 
    sub     => '1', 
    co      => co, 
    s       => s
    ); 
     
end Behavioral;
