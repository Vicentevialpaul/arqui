library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_unsigned.all;
-- Contador de Clock 
entity PC2 is
    Port ( clock    : in  std_logic;
           dataout  : out std_logic_vector (7 downto 0));
end PC2;

architecture Behavioral of PC2 is

signal pc : std_logic_vector(7 downto 0) := (others => '0');

begin

pc_prosses : process (clock)
    begin
      if (rising_edge(clock)) then
        pc <= pc + 1;
      end if;
    end process;
    
dataout <= pc;

end Behavioral;

