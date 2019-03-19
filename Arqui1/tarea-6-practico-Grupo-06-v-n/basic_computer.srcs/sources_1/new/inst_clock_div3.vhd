LIBRARY IEEE;
    USE IEEE.STD_LOGIC_1164.ALL;
    USE IEEE.NUMERIC_STD.ALL;
    
    ENTITY CLK_DIVIDER IS
        PORT(CLK_IN: IN STD_LOGIC;
            RESET: IN STD_LOGIC;
            CLK_OUT: OUT STD_LOGIC);
        END ENTITY;
        
        ARCHITECTURE BEV OF CLK_DIVIDER IS
            BEGIN
                PROCESS(CLK_IN,RESET)
                    VARIABLE COUNT : INTEGER:=0;
                    VARIABLE TEMP : STD_LOGIC:='0';
                    BEGIN
                        IF RESET='1' THEN
                            COUNT:=0;
                            TEMP:='0';
                        ELSIF RISING_EDGE(CLK_IN)THEN
                            COUNT:=COUNT+1;
                            IF COUNT=1 THEN
                                TEMP:= NOT TEMP;
                            END IF;
                            IF COUNT=2 THEN
                                TEMP:=NOT TEMP;
                            END IF;
                             IF COUNT=3 THEN
                                TEMP:= '0' ;
                                COUNT:=0;
                            END IF;
                        END IF;
                        CLK_OUT<=TEMP;
                        END PROCESS;
                    END BEV;