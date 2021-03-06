library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity Adder8_p_tb is
end;

architecture bench of Adder8_p_tb is

  component Adder8_p
      Port ( d_in : in STD_LOGIC_VECTOR (7 downto 0);
             s : out STD_LOGIC_VECTOR (7 downto 0));
  end component;

  signal d_in: STD_LOGIC_VECTOR (7 downto 0);
  signal s: STD_LOGIC_VECTOR (7 downto 0);

begin

  uut: Adder8_p port map ( d_in => d_in,
                           s    => s );

  stimulus: process
  begin
  
    -- Put initialisation code here
    d_in <= "01010101";

    -- Put test bench stimulus code here

    wait;
  end process;


end;
  