library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity Sub_ip_p_tb is
end;

architecture bench of Sub_ip_p_tb is

  component Sub_ip_p
      Port ( data_in : in STD_LOGIC_VECTOR (7 downto 0);
             s : out STD_LOGIC_VECTOR (7 downto 0));
  end component;

  signal data_in: STD_LOGIC_VECTOR (7 downto 0);
  signal s: STD_LOGIC_VECTOR (7 downto 0);

begin

  uut: Sub_ip_p port map ( data_in => data_in,
                           s       => s );

  stimulus: process
  begin
  
    -- Put initialisation code here
    data_in <= "00010110"; 


    -- Put test bench stimulus code here

    wait;
  end process;


end;
  
