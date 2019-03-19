import sys
lista_de_instrucciones = [] #lista de listas con las instrucciones
Sp = 255
lista_Sp = []
stack = []
W = 0
MuxS = 0
LoadReg = 1
Sop = ""
for i in range(256):
    stack.append(0)
def restar_a_indicador():
    global Sp
    if Sp == 0:
        Sp = 255
    else:
        Sp -= 1

def sumar_a_indicador():
    global Sp
    if Sp == 255:
        Sp = 0
    else:
        Sp += 1


def numero_a_binario_de_8_digitos(numero):
    binario = bin(numero)
    binario = binario[2:]
    while True:
        if len(binario) > 8:
            binario = binario[-8:]
        if len(binario) == 8:
            break
        else:
            binario = "0" +binario
    return binario

def binario_a_entero(binario):  #retorna int de binario
    return int(binario,2)

def not_binario(binario):  #pasar numero con 8 digitos
    retorno = ""
    for i in binario:
        if i == "1":
            retorno += "0"
        else:
            retorno += "1"
    return retorno


#print(not_binario(bin(5)))
#print(14 & 5 ) #AND
#print(14|5) #OR
#print(14^5) #XOR
#print(not(5))
#print(bin(255 << 1)) #SHL
#print(bin(4 >> 1)) #SHR
def abrir_archivo(archivo_entrada):
    lista_a_retornar = []
    archivo = open(archivo_entrada,"r")
    for linea in (archivo.readlines()):
        if ";" in linea or linea[0] == ";":
            pass
        else:
            lista_a_retornar.append(linea[0:-1])
    return lista_a_retornar


def PUSH_Lit(lit):

    global W
    global MuxS
    global stack
    global Sp
    tupla = []
    tupla.append("0000000000000")
    restar_a_indicador()
    lista_Sp.append(stack[Sp])
    agregar = "00001"
    numero = numero_a_binario_de_8_digitos(int(lit))
    agregar += numero
    tupla.append(agregar)
    lista_de_instrucciones.append(tupla)
    numero_agregar = binario_a_entero(numero)
    stack[Sp] = numero_agregar
    lista_Sp.append(stack[Sp])
    W = 1
    MuxS = 1

def POP():
    global Sp
    sumar_a_indicador()
    lista_de_instrucciones.append(["0001000000000"])
    lista_Sp.append(stack[Sp])

def ADD():
    global  LoadReg
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    sumar_a_indicador()
    tupla = []
    tupla.append("0001100000000")
    lista_Sp.append(stack[Sp])
    Sop = "ADD"
    W = 1
    MuxS = 0
    tupla.append("0010000000000")
    if Sp == 0:
        numero_1 = stack[0]
        numero_2 = stack[255]
        numero = numero_1 + numero_2
    else:
        numero_1 = stack[Sp]
        numero_2 = stack[Sp-1]
        numero = numero_1 + numero_2

    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)

def SUB():
    global  LoadReg
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    sumar_a_indicador()
    tupla = []
    tupla.append("0010100000000")
    lista_Sp.append(stack[Sp])
    Sop = "SUB"
    W = 1
    MuxS = 0
    tupla.append("0011000000000")
    if Sp == 0:
        numero_1 = stack[0]
        numero_2 = stack[255]
        numero = numero_1 - numero_2
    else:
        numero_1 = stack[Sp]
        numero_2 = stack[Sp-1]
        numero = numero_1 - numero_2
    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)


def AND():
    global  LoadReg
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    sumar_a_indicador()
    tupla = []
    tupla.append("0011100000000")
    lista_Sp.append(stack[Sp])
    Sop = "AND"
    W = 1
    MuxS = 0
    tupla.append("0100000000000")
    if Sp == 0:
        numero_1 = stack[0]
        numero_2 = stack[255]
        numero = numero_1 & numero_2
    else:
        numero_1 = stack[Sp]
        numero_2 = stack[Sp-1]
        numero = numero_1 & numero_2
    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)


def OR():
    global  LoadReg
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    sumar_a_indicador()
    tupla = []
    tupla.append("0100100000000")
    lista_Sp.append(stack[Sp])
    Sop = "OR"
    W = 1
    MuxS = 0
    tupla.append("0101000000000")
    if Sp == 0:
        numero_1 = stack[0]
        numero_2 = stack[255]
        numero = numero_1 | numero_2
    else:
        numero_1 = stack[Sp]
        numero_2 = stack[Sp-1]
        numero = numero_1 | numero_2
    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)


def XOR():
    global  LoadReg
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    sumar_a_indicador()
    tupla = []
    tupla.append("0101100000000")
    lista_Sp.append(stack[Sp])
    Sop = "XOR"
    W = 1
    MuxS = 0
    tupla.append("0110000000000")
    if Sp == 0:
        numero_1 = stack[0]
        numero_2 = stack[255]
        numero = numero_1 ^ numero_2
    else:
        numero_1 = stack[Sp]
        numero_2 = stack[Sp-1]
        numero = numero_1 ^ numero_2
    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)



def SHL():
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    tupla = []
    tupla.append("0110100000000")
    Sop = "SHL"
    W = 1
    MuxS = 0
    numero = stack[Sp]
    binario = bin(numero << 1)[2:]
    if len(binario) > 8:
        binario = binario[-8:]
    numero = binario_a_entero(binario)
    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)

def SHR():
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    tupla = []
    tupla.append("0111000000000")
    Sop = "SHR"
    W = 1
    MuxS = 0
    numero = stack[Sp]
    binario = bin(numero >> 1)
    numero = binario_a_entero(binario)
    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)

def NOT():
    global Sop
    global W
    global MuxS
    global Sp
    LoadReg = 1
    tupla = []
    tupla.append("0111100000000")
    Sop = "NOT"
    W = 1
    MuxS = 0
    numero = stack[Sp]
    binario = numero_a_binario_de_8_digitos(numero)
    binario = not_binario(binario)
    numero = binario_a_entero(binario)
    stack[Sp] = numero
    lista_Sp.append(stack[Sp])
    lista_de_instrucciones.append(tupla)

def NOP():
    global W
    W = 0
    lista_de_instrucciones.append(["1000000000000"])
    lista_Sp.append(stack[Sp])

def abrir_archivo_2(archivo_entrada):

    lista_a_retornar = []
    archivo_entrada = open(archivo_entrada,"r")
    for linea in (archivo_entrada.readlines()):
        lista_a_retornar.append(linea[0:-1])
    return lista_a_retornar

def simulacion(archivo_entrada):
    global contador
    archivo = abrir_archivo_2(archivo_entrada)

    for elemento in archivo:
        elemento1 = elemento[0:5]
        elemento2 = elemento[5:]
        if elemento1 == "00000":
            restar_a_indicador()
            lista_Sp.append(stack[Sp])
        if elemento1 == "00001":
            numero = elemento2
            numero_agregar = binario_a_entero(numero)
            stack[Sp] = numero_agregar
            lista_Sp.append(numero_agregar)
        if elemento1 == "00010":
            sumar_a_indicador()
            lista_Sp.append(stack[Sp])
        if elemento1 == "00011":
            sumar_a_indicador()
            lista_Sp.append(stack[Sp])
        if elemento1 == "00100":
            if Sp == 0:
                numero_1 = stack[0]
                numero_2 = stack[255]
                numero = numero_1 + numero_2
            else:
                numero_1 = stack[Sp]
                numero_2 = stack[Sp-1]
                numero = numero_1 + numero_2

            stack[Sp] = numero
            lista_Sp.append(stack[Sp])


        if elemento1 == "00101":
            sumar_a_indicador()
            lista_Sp.append(stack[Sp])
        if elemento1 == "00110":
            if Sp == 0:
                numero_1 = stack[0]
                numero_2 = stack[255]
                numero = numero_1 - numero_2
            else:
                numero_1 = stack[Sp]
                numero_2 = stack[Sp-1]
                numero = numero_1 - numero_2

            stack[Sp] = numero
            lista_Sp.append(stack[Sp])



        if elemento1 == "00111":
            sumar_a_indicador()
            lista_Sp.append(stack[Sp])
        if elemento1 == "01000":
            if Sp == 0:
                numero_1 = stack[0]
                numero_2 = stack[255]
                numero = numero_1 & numero_2
            else:
                numero_1 = stack[Sp]
                numero_2 = stack[Sp-1]
                numero = numero_1 & numero_2
            stack[Sp] = numero
            lista_Sp.append(stack[Sp])

        if elemento1 == "01001":
            sumar_a_indicador()
            lista_Sp.append(stack[Sp])
        if elemento1 == "01010":
            if Sp == 0:
                numero_1 = stack[0]
                numero_2 = stack[255]
                numero = numero_1 | numero_2
            else:
                numero_1 = stack[Sp]
                numero_2 = stack[Sp-1]
                numero = numero_1 | numero_2
            stack[Sp] = numero
            lista_Sp.append(stack[Sp])

        if elemento1 == "01011":
            sumar_a_indicador()
            lista_Sp.append(stack[Sp])
        if elemento1 == "01100":
            if Sp == 0:
                numero_1 = stack[0]
                numero_2 = stack[255]
                numero = numero_1 ^ numero_2
            else:
                numero_1 = stack[Sp]
                numero_2 = stack[Sp-1]
                numero = numero_1 ^ numero_2
            stack[Sp] = numero
            lista_Sp.append(stack[Sp])
        if elemento1 == "01101":
            SHL()
        if elemento1 == "01110":
            SHR()
        if elemento1 == "01111":
            NOT()
        if elemento1 == "10000":
            NOP()
    archivo = open(sys.argv[2],"w")
    for i in range(len(lista_Sp)):
        archivo.write("t = "+str(i) + "  " + numero_a_binario_de_8_digitos(lista_Sp[i]) + " " + str(lista_Sp[i])+"\n")
archivo_entrada = sys.argv[1]
simulacion(archivo_entrada)
