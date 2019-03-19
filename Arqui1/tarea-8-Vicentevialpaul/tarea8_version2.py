
import json
from ast import literal_eval

#prueba = json.loads("[[1,256, 256,487, 1001, 784, 256, 100,54,135,137,129, 128, 876, 342, 785, 251,251, 127, 257, 257, 367, 487, 586, 401,38,750,7,3,5,-1,843, 65, 87,2,1, 1001]]")
#PROG = prueba

# usar global en definiciones para asegurar..
#MEM_FIS_SIZE = 512 # puede ser la virtual
#MEM_VIR_SIZE = 1024
#PAGE_SIZE = 32
#TLB_LINE = 4
TLB = []
#CACHE_SIZE = 128
#CACHE_LINE = 16
#N_WAY_CACHE = 4
#NUM_PROG = 1
cache = []
tiempo = 1
tabla_de_paginas = None


MEM_FIS_SIZE = int(input())
MEM_VIR_SIZE = int(input())
PAGE_SIZE = int(input())
TLB_LINE = int(input())
CACHE_SIZE = int(input())
CACHE_LINE = int(input())
N_WAY_CACHE = int(input())
NUM_PROG = int(input())
PROG = json.loads(input())
#PROG = literal_eval(PROG)


def imprimir_tabla_paginas(tabla):
    for i in tabla:
        print("Numero Programa " + str(i))
        print("Pagina   Marco  Validez   Disco  Tiempo acceso")
        for j in tabla[i]:
            print(j)


def imprimir_cache():
    for i in cache:
        print("conjunto " + str(i))
        for j in cache[i]:
            print(str(j))

def imprimir_TLB():
    print("TLB")
    print("numero entrada     pagina     marco      tiempo")
    for i in TLB:
        print(i)
def generar_cache():

    global CACHE_SIZE
    global CACHE_LINE
    global N_WAY_CACHE
    global MEM_FIS_SIZE
    global tiempo
    palabras_por_linea = CACHE_SIZE/CACHE_LINE
    cantidad_conjuntos = CACHE_LINE/N_WAY_CACHE
    cache = dict()
    for i in range(int(cantidad_conjuntos)):
        lista_a_ingresar = []
        for j in range(N_WAY_CACHE):
            lista_a_ingresar.append([None, 0, None, 0, tiempo])
        cache[i] = lista_a_ingresar
    return cache

def numero_a_potencia_de_2(numero):
    numero = numero
    exponencial = 1
    while True:
        if numero == 2:
            break
        else:
            numero = numero/2
            exponencial += 1
    return exponencial

def generar_tabla_de_paginas():

    bits_pagina_virtual = numero_a_potencia_de_2(int(MEM_VIR_SIZE))
    bits_pagina = numero_a_potencia_de_2(int(PAGE_SIZE))  #palabras por pagina
    bits_numero_paginas_posibles = bits_pagina_virtual - bits_pagina
    numero_paginas_posibles = 2**(int(bits_numero_paginas_posibles))
    diccionario = dict()
    for i in range(len(PROG)):  # O PRUEBA
        numero = i  # se puede cambiar para coherencia, pero por ahora sera programa en posicion 0
        lista_a_guardar = []
        for j in range(int(numero_paginas_posibles)):
            lista_a_guardar.append([j, None, 0, 0, 0])
        diccionario[numero] = lista_a_guardar
    return diccionario

def generar_estadisticas():

    diccionario = dict()
    for i in range(len(PROG)):
        numero = i
        diccionario[numero] = [0, 0, 0, 0, 0, 0, 0]
    return diccionario

estadisticas = generar_estadisticas()
tabla_de_paginas = generar_tabla_de_paginas()




def generar_registro_posicion_lista():

    diccionario = dict()
    contador = 0
    for lista in PROG:
        diccionario[contador] = 0
        contador += 1
    return(diccionario)




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

def generar_direccion_pagina_virtual(numero):

    numero_bits = numero_a_potencia_de_2(int(MEM_VIR_SIZE)) # es de ser de virtual..
    binario = bin(numero)
    binario = binario[2:]
    while True:
        if len(binario) > numero_bits:
            binario = binario[-(numero_bits):]
        if len(binario) == numero_bits:
            break
        else:
            binario = "0" +binario
    return binario

def generar_direccion_marco(numero):

    numero_bits = numero_a_potencia_de_2(int(MEM_FIS_SIZE/PAGE_SIZE))
    binario = bin(numero)
    binario = binario[2:]
    while True:
        if len(binario) > numero_bits:
            binario = binario[-(numero_bits):]
        if len(binario) == numero_bits:
            break
        else:
            binario = "0" +binario
    return binario


def generar_TLB():
    global TLB
    global tiempo
    TLB = []
    for i in range(TLB_LINE):
        TLB.append([i, None, None, tiempo])   # ojo con None para revisar
    return TLB

def agregar_a_TLB(lista_estilo_TLB):
    global TLB
    minimo = 1000000000000000000000000000
    minimo_a_poner = None #indice lista
    espacio_a_poner = None
    for lista in range(len(TLB)):
        if espacio_a_poner == None:
            if TLB[lista][1] == None and TLB[lista][2] == None:
                TLB[lista] = lista_estilo_TLB
                espacio_a_poner = True
            else:
                if TLB[lista][3] < minimo:
                    minimo_a_poner = lista #indicie lista
                    minimo = TLB[lista][3]
    if espacio_a_poner == None:
        TLB[minimo_a_poner] = lista_estilo_TLB
    else:
        pass
    return True

def existe_en_TLB(numero_pagina):

    global TLB
    global tiempo
    for linea in TLB:
        if linea[1] == numero_pagina:
            linea[3] = tiempo
            return linea[2]
    return False

def es_valido_en_tabla(numero_pagina, numero_programa):

    global tabla_de_paginas
    global tiempo
    for linea in tabla_de_paginas:
        if linea == numero_programa:
            for lista in tabla_de_paginas[linea]:
                if lista[0] == numero_pagina:
                    lista[4] = tiempo
                    if lista[2] == 1:
                        return lista[1], lista[3]
                    else:
                        return False, False
    return False, False # error...

def asignar_marco(numero_pagina, numero_programa):

    global tabla_de_paginas
    global estadisticas
    global tiempo
    numero_marcos = MEM_FIS_SIZE/PAGE_SIZE
    contador = 0   # marco en 1 o 0
    marco_a_poner = None
    ##   revisa si existen marcos disponibles
    while contador < numero_marcos: # dependiendo de marco en 1 o 0
        existe_marco = 0
        for programa in tabla_de_paginas:
            num_prog = programa
            lista_paginas = tabla_de_paginas[programa]
            for pagina in range(len(lista_paginas)):
                if lista_paginas[pagina][1] == contador: #tiempo de acceso  # podria chequearse si esta en disco o no
                    existe_marco = 1
        if existe_marco == 0:
            marco_a_poner = contador
            break
        else:
            contador += 1
    if marco_a_poner != None:        #     existe marco a asignar
        programa_a_cambiar = tabla_de_paginas[numero_programa]
        pagina_a_cambiar = programa_a_cambiar[numero_pagina]
        pagina_a_cambiar[2] = 1
        pagina_a_cambiar[1] = marco_a_poner
        pagina_a_cambiar[4] = tiempo
        tabla_de_paginas[numero_programa][numero_pagina] = pagina_a_cambiar
    else:    #no existe marco a asignar, se saca el que se uso ultimo a disco y se hace espacio
        #print("marco lleno")
        minimo = 90000000000000000000000000000000000000000000000000
        contenido_minimo = None
        for programa in tabla_de_paginas:
            num_prog = programa
            lista_paginas = tabla_de_paginas[programa]
            # ver cual marco reemplazar de memoria
            for pagina in range(len(lista_paginas)):
                if lista_paginas[pagina][4] < minimo and lista_paginas[pagina][2] == 1 and lista_paginas[pagina][3] == 0:   #tiempo de acceso Y bit validez
                    minimo = lista_paginas[pagina][4]
                    contenido_minimo = [num_prog, pagina]   # ojo si se cambia numero programa
        # cambiar programa que hace swap out
        programa_a_cambiar = tabla_de_paginas[contenido_minimo[0]]
        pagina_a_cambiar = programa_a_cambiar[contenido_minimo[1]]
        pagina_a_cambiar[3] = 1 # ojo si se genera cambio.. si hay cambio..
        tabla_de_paginas[contenido_minimo[0]][contenido_minimo[1]] = pagina_a_cambiar
        lista_a_cambiar = estadisticas[contenido_minimo[0]]
        lista_a_cambiar[4] = lista_a_cambiar[4] + 1   #swap out
        estadisticas[contenido_minimo[0]] = lista_a_cambiar
        # cambiar programa que hace swap out
        #agregar marco escogido, ojo si se cambia algo
        numero_marco = pagina_a_cambiar[1]
        programa_a_cambiar = tabla_de_paginas[numero_programa]
        pagina_a_cambiar = programa_a_cambiar[numero_pagina]
        pagina_a_cambiar[2] = 1
        pagina_a_cambiar[1] = numero_marco   # se podria usar copy......
        pagina_a_cambiar[4] = tiempo
        tabla_de_paginas[numero_programa][numero_pagina] = pagina_a_cambiar
    return True


def disco_a_marco(numero_pagina, numero_programa):
    global tabla_de_paginas
    global estadisticas
    minimo = 90000000000000000000000000000000000000000000000000
    contenido_minimo = None
    for programa in tabla_de_paginas:
        num_prog = programa
        lista_paginas = tabla_de_paginas[programa]
        for pagina in range(len(lista_paginas)):
            if lista_paginas[pagina][4] < minimo and lista_paginas[pagina][2] == 1 \
                    and lista_paginas[pagina][3] == 0:   #tiempo de acceso
                minimo = lista_paginas[pagina][4]
                contenido_minimo = [num_prog, pagina]
    # cambiar programa que hace swap out
    programa_a_cambiar = tabla_de_paginas[contenido_minimo[0]]
    pagina_a_cambiar = programa_a_cambiar[contenido_minimo[1]]
    pagina_a_cambiar[3] = 1
    tabla_de_paginas[contenido_minimo[0]][contenido_minimo[1]] = pagina_a_cambiar
    lista_a_cambiar = estadisticas[contenido_minimo[0]]
    lista_a_cambiar[4] = lista_a_cambiar[4] + 1   #swap out
    estadisticas[contenido_minimo[0]] = lista_a_cambiar
    # cambiar programa que hace swap out
    #agregar marco a pagina actual
    numero_marco = pagina_a_cambiar[1]
    programa_a_cambiar = tabla_de_paginas[numero_programa]
    pagina_a_cambiar = programa_a_cambiar[numero_pagina]
    pagina_a_cambiar[3] = 0
    pagina_a_cambiar[1] = numero_marco
    tabla_de_paginas[numero_programa][numero_pagina] = pagina_a_cambiar
    return True


def generar_direccion_pagina_fisica(direccion_virtual, numero_programa):
    global estadisticas
    global TLB
    numero_marcos = int(MEM_FIS_SIZE/PAGE_SIZE)
    bits_pagina_virtual = numero_a_potencia_de_2(int(MEM_VIR_SIZE))
    bits_pagina = numero_a_potencia_de_2(int(PAGE_SIZE))  #palabras por pagina
    bits_numero_paginas_posibles = bits_pagina_virtual - bits_pagina
    numero_bin_pagina = direccion_virtual[0:bits_numero_paginas_posibles]
    numero_pagina = int(numero_bin_pagina,2) # numero binario de pagina
    marco = existe_en_TLB(numero_pagina)
    if marco is not False: # marco se encuentra en TLB
        tabla_de_paginas[numero_programa][numero_pagina][4] = tiempo
        direccion_marco = generar_direccion_marco(marco)
        direccion_pagina_fisica = direccion_marco + direccion_virtual[bits_numero_paginas_posibles:] #ofset
        lista_a_cambiar = estadisticas[numero_programa]
        lista_a_cambiar[0] = lista_a_cambiar[0] + 1   #hit TLB
        estadisticas[numero_programa] = lista_a_cambiar
        return direccion_pagina_fisica
    else:   #direccion no esta en TLB
        #BUSCAR PAGINA EN TABLA DE PROGRAMA
        tabla_de_paginas[numero_programa][numero_pagina][4] = tiempo
        marco, disco = (es_valido_en_tabla(numero_pagina,numero_programa))
        if marco is not False: # pagina es valida
            # puede estar guardado en disco o no
            if disco == 0: #guardado en memoria
                direccion_marco = generar_direccion_marco(marco)
                direccion_pagina_fisica = direccion_marco + direccion_virtual[bits_numero_paginas_posibles:]
                agregar_a_TLB([tiempo,numero_pagina,marco,tiempo])
                return direccion_pagina_fisica
            else: #guardado en disco
                #print("guardado en disco")
                lista_a_cambiar = estadisticas[numero_programa]
                lista_a_cambiar[2] = lista_a_cambiar[2] + 1   #page fault, cuando esta guardada en disco
                lista_a_cambiar[3] = lista_a_cambiar[3] + 1   #swap in, falta swap out (esta en disco_a_marco)
                estadisticas[numero_programa] = lista_a_cambiar
                disco_a_marco(numero_pagina, numero_programa)
                # ya esta en memoria
                marco, disco = es_valido_en_tabla(numero_pagina, numero_programa) # por ejecucion si o si es valido y esta en memoria
                direccion_marco = generar_direccion_marco(marco)
                direccion_pagina_fisica = direccion_marco + direccion_virtual[bits_numero_paginas_posibles:]
                agregar_a_TLB([tiempo,numero_pagina,marco,tiempo])
                return direccion_pagina_fisica
        else:    #pagina no es valida
            asignar_marco(numero_pagina, numero_programa)
            #ya se asigno marco y validez
            marco, disco = es_valido_en_tabla(numero_pagina, numero_programa) # por ejecucion si o si es valido y esta en memoria
            direccion_marco = generar_direccion_marco(marco)
            direccion_pagina_fisica = direccion_marco + direccion_virtual[bits_numero_paginas_posibles:]
            agregar_a_TLB([tiempo,numero_pagina,marco,tiempo])
            lista_a_cambiar = estadisticas[numero_programa]
            lista_a_cambiar[2] = lista_a_cambiar[2] + 1   #page fault, cuando no esta en memoria
            #lista_a_cambiar[4] = lista_a_cambiar[4] + 1   swap out cuando no esta en memoria..
            estadisticas[numero_programa] = lista_a_cambiar
            return direccion_pagina_fisica


def buscar_en_cache(direccion_fisica, numero_programa):

    global CACHE_SIZE
    global CACHE_LINE
    global N_WAY_CACHE
    global MEM_FIS_SIZE
    global cache
    global tiempo
    global estadisticas
    global tabla_de_paginas
    palabras_por_linea = int(CACHE_SIZE/CACHE_LINE)
    cantidad_conjuntos = int(CACHE_LINE/N_WAY_CACHE)
    bits_posicion = numero_a_potencia_de_2(int(palabras_por_linea))
    bits_conjunto = numero_a_potencia_de_2(int(cantidad_conjuntos))
    bits_tag = numero_a_potencia_de_2(int(MEM_FIS_SIZE)) - bits_posicion - bits_conjunto
    tag_direccion = direccion_fisica[0:bits_tag]
    numero_de_conjunto = direccion_fisica[bits_tag:bits_tag + bits_conjunto]   #CAMBIAR EN DEMAS
    numero_posicion = direccion_fisica[bits_tag + bits_conjunto:] # cambiar en demas
    #print("bits tag: "+ str(tag_direccion)+ " " + "bit conjunto: " + str(numero_de_conjunto) + " bits posicion: " + str(numero_posicion))
    numero_de_conjunto = int(numero_de_conjunto,2)
    numero_posicion = int(numero_posicion,2)  # error
    conjunto = cache[numero_de_conjunto] #actualizar conjunto, ojo con copy..
    encontrado = "no"
    for linea in range(len(conjunto)):
        tag = conjunto[linea][2]
        if tag == tag_direccion:
            encontrado = "si"
            conjunto[linea][3] = conjunto[linea][3] + 1
    if encontrado == "si":
        cache[numero_de_conjunto] = conjunto
        lista_a_cambiar = estadisticas[numero_programa]
        lista_a_cambiar[1] = lista_a_cambiar[1] + 1   #hit TLB
        estadisticas[numero_programa] = lista_a_cambiar
        return "encontrado en cache"
    else:   # se busca en memoria, y se reemplaza en cache
        espacio_vacio = "no"
        for linea in range(len(conjunto)):
            bit_validez = conjunto[linea][1]
            if bit_validez == 0 and espacio_vacio == "no":
                conjunto[linea][1] = 1
                conjunto[linea][2] = tag_direccion
                conjunto[linea][3] = 1 #cantidad de accesos
                conjunto[linea][4] = tiempo  #tiempo
                espacio_vacio = "si"
        if espacio_vacio == "no": #no hay espacio en cache se reemplaza
            lista_candidatos_a_salir = []
            minimo = 99999999999999999999999999999999999999999
            for linea in range(len(conjunto)):
                if conjunto[linea][3] < minimo:
                    minimo = conjunto[linea][3]
            for linea in range(len(conjunto)):
                if conjunto[linea][3] == minimo:
                    lista_candidatos_a_salir.append(linea)
            if len(lista_candidatos_a_salir) == 0:
                print("error")
            if len(lista_candidatos_a_salir) == 1:
                salir_cache = lista_candidatos_a_salir[0]
                conjunto[salir_cache][3] = 1
                conjunto[salir_cache][2] = tag_direccion
                conjunto[salir_cache][4] = tiempo  #tiempo
            if len(lista_candidatos_a_salir) > 1:
                minimo = 99999999999999999999999999999999999999999
                elemento_a_cambiar = 0
                for candidato in lista_candidatos_a_salir:
                    if conjunto[candidato][4] < minimo:
                        minimo = conjunto[candidato][4]
                        elemento_a_cambiar = candidato
                conjunto[elemento_a_cambiar][2] = tag_direccion
                conjunto[elemento_a_cambiar][3] = 1 #cantidad de accesos
                conjunto[elemento_a_cambiar][4] = tiempo  #tiempo


        return True


def simulacion():   # termino es cuando no quedan programas por ejecutar
    global TLB
    global estadisticas
    global tabla_de_paginas
    global tiempo
    global cache
    diccionario_registro = generar_registro_posicion_lista()
    numero_paginas = 0
    estadisticas = generar_estadisticas()
    tabla_de_paginas = generar_tabla_de_paginas()
    numero_lista_actual = 0
    numero_programas = NUM_PROG
    salida = []
    while True: # recorre lista de programas
        TLB = generar_TLB()  # va a reiniciar TLB para cada programa.
        cache = generar_cache()
        lista_actual = PROG[numero_lista_actual]
        while True:  #recorre programa
            #print(numero_lista_actual)
            posicion_actual = diccionario_registro[numero_lista_actual]
            if posicion_actual >= len(lista_actual):
                tiempo += 1
                if numero_lista_actual not in salida:
                    salida.append(numero_lista_actual)
                break
            else:
                valor_actual = lista_actual[posicion_actual]
                if valor_actual == -1:
                    tiempo += 1
                    diccionario_registro[numero_lista_actual] = diccionario_registro[numero_lista_actual] + 1
                    break
                else:
                    direccion = valor_actual
                    direccion_pagina_virtual = generar_direccion_pagina_virtual(direccion)
                    direccion_fisica = generar_direccion_pagina_fisica(direccion_pagina_virtual, numero_lista_actual)
                    #print("direccion pagina virtual : " + str(direccion_pagina_virtual))
                    #print("direccion fisica : " + str(direccion_fisica))
                    buscar_en_cache(direccion_fisica,numero_lista_actual)
                    #print("cache")
                    #imprimir_cache()
                    diccionario_registro[numero_lista_actual] = diccionario_registro[numero_lista_actual] + 1
                    tiempo += 1
            #imprimir_tabla_paginas(tabla_de_paginas)
            #imprimir_TLB()
        if int(numero_lista_actual) >= int(NUM_PROG) - 1:
            numero_lista_actual = 0
        else:
            numero_lista_actual += 1
        if len(salida) == NUM_PROG:
            break


def estadisticas_paginas():
    global estadisticas
    for i in tabla_de_paginas:
        paginas_validas = 0
        paginas_en_disco = 0
        for j in tabla_de_paginas[i]:
            if j[2] == 1 and j[3] ==0:
                paginas_validas += 1
            if j[2] == 1 and j[3] == 1:
                paginas_en_disco += 1
        estadisticas[i][5] = paginas_validas
        estadisticas[i][6] = paginas_en_disco
    return True

def imprimir_estadisticas():
    for i in estadisticas:
        print("PROGRAMA "+str(i+1))
        print("hit TLB: " + str(estadisticas[i][0]))
        print("hit cache: " + str(estadisticas[i][1]))
        print("page fault: " + str(estadisticas[i][2]))
        print("swapp in: " + str(estadisticas[i][3]))
        print("swapp out: " + str(estadisticas[i][4]))
        print("page valid: " + str(estadisticas[i][5]))
        print("page disk: " + str(estadisticas[i][6]))
        print(" ")



simulacion()
#imprimir_tabla_paginas(tabla_de_paginas)
estadisticas_paginas()
imprimir_estadisticas()
#print(tabla_de_paginas)
#print(estadisticas)
