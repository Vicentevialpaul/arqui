----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/13/2017 07:55:53 PM
-- Design Name: 
-- Module Name: sim1 - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------


library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity sim1 is
--  Port ( );
end sim1;

architecture Behavioral of sim1 is

component Basys3
    Port (
        sw          : in   std_logic_vector (3 downto 0);
        btn         : in   std_logic_vector (4 downto 0);
        led         : out  std_logic_vector (3 downto 0);
        clk         : in   std_logic;
        seg         : out  std_logic_vector (7 downto 0);
        an          : out  std_logic_vector (3 downto 0)
    );
end component;

signal sw  : std_logic_vector(3 downto 0)  := (others => '0');
signal btn : std_logic_vector (4 downto 0)  := (others => '0'); 
signal led : std_logic_vector (3 downto 0) := (others => '0'); 
signal clk : std_logic := '0';                     
signal seg : std_logic_vector (7 downto 0)  := (others => '0');  
signal an  : std_logic_vector (3 downto 0)  := (others => '0');

BEGIN
 inst_Basys: Basys3 port map (sw, btn, led, clk, seg, an);
 proc: process
 begin 
     btn <= "01010";
     sw <= "1001";
     clk <= '0';
     L1: loop
         if clk = '0' then
             clk <= '1';
         else
             clk <= '0';
         end if;
         wait for 10 ns;
     end loop L1;
 wait;
 end process proc;
END Behavioral;