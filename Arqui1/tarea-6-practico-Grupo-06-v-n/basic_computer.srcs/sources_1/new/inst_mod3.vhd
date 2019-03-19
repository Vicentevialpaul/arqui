library IEEE;
use IEEE.STD_LOGIC_1164.ALL;


entity mod3 is
    Port ( data_in  : in STD_LOGIC_VECTOR (7 downto 0);
           data_out : out  std_logic);
end mod3;

architecture Behavioral of mod3 is

component Sub_ip_p
     Port ( data_in : in STD_LOGIC_VECTOR (7 downto 0);
          s : out STD_LOGIC_VECTOR (7 downto 0));
     end component; 

signal result : std_logic_vector(7 downto 0); 

begin
                
inst_Sub_ip_p: Sub_ip_p port map( 
    data_in     =>data_in,
    s           =>result
    ); 

with result select
    data_out <= '1' when "00000000", -- 0
                '1' when "00000011", -- 3
                '1' when "11111101", -- -3
                '0' when others;

end Behavioral;
