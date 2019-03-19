library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity mod3_tb is
end;

architecture bench of mod3_tb is

  component mod3
      Port ( data_in  : in STD_LOGIC_VECTOR (7 downto 0);
             data_out : out  std_logic);
  end component;

  signal data_in: STD_LOGIC_VECTOR (7 downto 0);
  signal data_out: std_logic;

begin

  uut: mod3 port map ( data_in  => data_in,
                       data_out => data_out );

  stimulus: process
  begin
  
    -- Put initialisation code here

    data_in <= "00101010"; 
   

    -- Put test bench stimulus code here

    wait;
  end process;


end;
  
