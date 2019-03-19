a=bin(1)
print(a[1:])

inputA =  1   # define la entrada de secuencia binaria A
inputB =  2  # define la secuencia binaria inputB

print(bin(1))
print(bin(2))

inputA = int('00100011',2)
inputB = int('00101101',2)

print(bin(inputA))
print(bin(inputB))
print(bin(inputA | inputB))


def binario_a_8_digitos(binario):
    binario = str(binario)
    binario = binario[2:]
    while True:
        if len(binario) == 8:
            break
        else:
            binario = "0" +binario
    return binario

def binario_a_decimal(binario):
    return int(binario,2)
a = (binario_a_8_digitos(a))
print(int("00110",2))


a = "123456789"
print(a[-8:])


print("and")
print(14 & 5 ) #AND
print(14|5) #OR
print("xor")
print(14^5) #XOR
print(not(5))

print(bin(5 << 1)[2:]) #SHL
print(bin(4))
print(bin(4 >> 1)) #SHR

def abrir_archivo(archivo_entrada):
    lista_a_retornar = []
    archivo = open(archivo_entrada,"r")
    for linea in (archivo.readlines()):
        if ";" in linea or linea[0] == ";" or linea == "":
            pass
        else:
            lista_a_retornar.append(linea[0:-1])
    return lista_a_retornar

print(abrir_archivo("program.txt"))

binario = "100000001"
print(binario[-8:])
print(int("0011",2))
