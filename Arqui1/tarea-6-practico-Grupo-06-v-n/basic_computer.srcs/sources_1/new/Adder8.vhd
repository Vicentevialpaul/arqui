----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 09/25/2018 12:51:26 PM
-- Design Name: 
-- Module Name: Adder8 - Behavioral
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

entity Adder8 is
    Port ( a : in STD_LOGIC_VECTOR (7 downto 0);
           b : in STD_LOGIC_VECTOR (7 downto 0);
           ci : in STD_LOGIC;
           s : out STD_LOGIC_VECTOR (7 downto 0);
           co : out STD_LOGIC);
end Adder8;

architecture Behavioral of Adder8 is

component FA
    Port ( a  : in  std_logic;
           b  : in  std_logic;
           ci : in  std_logic;
           s  : out std_logic;
           c  : out std_logic);
    end component;

signal c : std_logic_vector(6 downto 0);

begin

inst_FA0: FA port map(
        a      =>a(0),
        b      =>b(0),
        ci     =>ci,
        s      =>s(0),
        c      =>c(0)
    );
    
inst_FA1: FA port map(
        a      =>a(1),
        b      =>b(1),
        ci     =>c(0),
        s      =>s(1),
        c      =>c(1)
    );

inst_FA2: FA port map(
        a      =>a(2),
        b      =>b(2),
        ci     =>c(1),
        s      =>s(2),
        c      =>c(2)
    );

inst_FA3: FA port map(
        a      =>a(3),
        b      =>b(3),
        ci     =>c(2),
        s      =>s(3),
        c      =>c(3)
    );

inst_FA4: FA port map(
        a      =>a(4),
        b      =>b(4),
        ci     =>c(3),
        s      =>s(4),
        c      =>c(4)
    );
    
inst_FA5: FA port map(
        a      =>a(5),
        b      =>b(5),
        ci     =>c(4),
        s      =>s(5),
        c      =>c(5)
    );

inst_FA6: FA port map(
        a      =>a(6),
        b      =>b(6),
        ci     =>c(5),
        s      =>s(6),
        c      =>c(6)
    );

inst_FA7: FA port map(
        a      =>a(7),
        b      =>b(7),
        ci     =>c(6),
        s      =>s(7),
        c      =>co
    );

end Behavioral;
