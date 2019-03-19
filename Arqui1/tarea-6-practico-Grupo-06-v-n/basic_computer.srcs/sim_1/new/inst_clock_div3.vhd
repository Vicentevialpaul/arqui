library IEEE;
use IEEE.Std_logic_1164.all;
use IEEE.Numeric_Std.all;

entity CLK_DIVIDER_tb is
end;

architecture bench of CLK_DIVIDER_tb is

      component CLK_DIVIDER
          PORT(CLK_IN: IN STD_LOGIC;
              RESET: IN STD_LOGIC;
              CLK_OUT: OUT STD_LOGIC);
          end component;

  signal CLK_IN: STD_LOGIC;
  signal RESET: STD_LOGIC;
  signal CLK_OUT: STD_LOGIC;

  constant clock_period: time := 10 ns;
  signal stop_the_clock: boolean;

begin

  uut: CLK_DIVIDER port map ( CLK_IN  => CLK_IN,
                              RESET   => RESET,
                              CLK_OUT => CLK_OUT );

 RESET <= '0';

  clocking: process
  begin
    while not stop_the_clock loop
      CLK_IN <= '0', '1' after clock_period / 2;
      wait for clock_period;
    end loop;
    wait;
  end process;

end;