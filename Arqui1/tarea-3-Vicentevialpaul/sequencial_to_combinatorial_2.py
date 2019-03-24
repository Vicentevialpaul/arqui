import json
datos = { "sequential": [ {"from": "input1", "to": "ffd1", "gate": "C"}, {"from": "ffd1", "gate": "Q", "to": "not1"},
                          {"from": "ffd1", " gate ": "Q", "to": "out1"},
                          {"from": "not1", "to": "ffd1", "gate": "D"},{"from": "input1", "to": "ffd2", "gate": "C"},
                          {"from": "ffd2", "gate": "Q", "to": "not2"},
                          {"from": "ffd2", " gate ": "Q", "to": "out2"},
                          {"from": "not2", "to": "ffd2", "gate": "D"}] }
#print(datos)
strings = json.dumps(datos)
nuevo = json.loads(strings, object_hook=lambda dict_obj: [(key, value) for key, value in dict_obj.items()])
#print(datos)
for i in nuevo[0][1]:
    pass

nuevo = nuevo[0][1]

contador_and = 0
contador_or = 0
contador_not = 0
lista_flip_flop = []
lista_flip_flop_nombres = []
secuencia_nueva = []
# “and{k}” “or{l}”  “not{n}” “ffd{s}”


class FlipFlop:

    def __init__(self, nombre = None, and_entrada_1 = None, not_entrada = None,
                 and_entrada_2 = None, not_salida = None):

        self.nombre_flip_flop = nombre
        self.and_entrada_1 = and_entrada_1  #elemento que recibe a D
        self.not_entrada = not_entrada  #elemento que recibe a C
        self.and_entrada_2 = and_entrada_2
        self.not_salida_Q = not_salida #elemento que recibe salida Q
        self.Q = None


def reemplazar_and():
    global contador_and
    contador_and += 1
    return "and" + str(contador_and)


def reemplazar_or():
    global contador_or
    contador_or += 1
    return "or" + str(contador_or)


def reemplazar_not():
    global contador_not
    contador_not += 1
    return "not"+ str(contador_not)

def setear_and():
    global contador_and
    for i in nuevo:
        for j in i:

            if j[1][0:3] == "and":
                contador_and = int(j[1][3:])
def setear_or():
    global contador_or
    for i in nuevo:
        for j in i:

            if j[1][0:2] == "or":
                contador_and = int(j[1][2:])
def setear_not():
    global contador_not
    for i in nuevo:
        for j in i:
            if j[1][0:3] == "not":
                contador_not = int(j[1][3:])

def reemplazar_from_sin_ffd(conector):
            if conector[0:2] == "in":
                return("from",conector)
            if conector[0:2]  == "no":
                return (("from", conector))
            if conector[0:2]  == "or":
                return (("from", conector))
            if conector[0:2]  == "an":
                return (("from", conector))


def generar_flip_flop_combinacional(nombre_flip_flop):
    global lista_flip_flop
    global lista_flip_flop_nombres
    global secuencia_nueva
    elemento_1 = (reemplazar_and())
    elemento_2 = (reemplazar_not())
    elemento_3 = (reemplazar_and())
    elemento_4 = (reemplazar_not())
    elemento_5 = (reemplazar_and())
    elemento_6 = (reemplazar_not())
    elemento_7 = (reemplazar_and())
    elemento_8 = (reemplazar_not())
    elemento_9 = (reemplazar_not())
    primer_and = [("from",elemento_1),("to",elemento_2)]
    primer_not = [("from",elemento_2),("to",elemento_3)]
    segundo_and = [("from",elemento_3),("to",elemento_9)]
    segundo_not = [("from", elemento_4), ("to",elemento_5)]
    tercer_and = [("from", elemento_5), ("to",elemento_6)]
    tercer_not = [("from", elemento_6), ("to",elemento_7)]
    cuarto_and = [("from", elemento_7), ("to",elemento_8)]
    cuarto_not = [("from", elemento_8), ("to",elemento_3)]
    conexion_Q = [("from", "Q"+nombre_flip_flop[3:]), ("to",elemento_7)]
    conexion_Q_2 = [("from", elemento_9),("to", "Q"+nombre_flip_flop[3:])]
    flip_flop = FlipFlop(nombre_flip_flop,elemento_1, elemento_4, elemento_5, elemento_9)
    lista_flip_flop.append(flip_flop)
    lista_flip_flop_nombres.append(nombre_flip_flop)
    secuencia_nueva.append(primer_and)
    secuencia_nueva.append(primer_not)
    secuencia_nueva.append(segundo_and)
    secuencia_nueva.append(segundo_not)
    secuencia_nueva.append(tercer_and)
    secuencia_nueva.append(tercer_not)
    secuencia_nueva.append(cuarto_and)
    secuencia_nueva.append(cuarto_not)
    secuencia_nueva.append(conexion_Q)
    secuencia_nueva.append(conexion_Q_2)
    return (primer_and, primer_not, segundo_and, segundo_not, tercer_and, tercer_not,
            cuarto_and, cuarto_not)

def agregar_elemento_a_flip_flop(nombre_flip, puerta, conexión):
    flip = None
    for flip_flop in lista_flip_flop:
        if flip_flop.nombre_flip_flop == nombre_flip:
            flip = flip_flop
    if puerta == "Q":
        return [("from",flip.not_salida_Q),("to",conexión)] #cambio
    if puerta == "D":
        return [("from",conexión),("to",flip.and_entrada_1)],[("from",conexión),("to",flip.not_entrada)]
    if puerta == "C":
        return [("from",conexión),("to",flip.and_entrada_2)],[("from",conexión),("to",flip.and_entrada_1)]

    

def reemplazo_secuencia(lista_secuencia):  #le llega una lista,retora lista con listas de tuplas a agregar
    lista_general = []
    lista_detalle = []
    for i in lista_secuencia:
        if i[0][1][0:2] != "ff":
            agregar = reemplazar_from_sin_ffd(i[0][1])
            lista_detalle.append(agregar)
            if i[1][1][0:2] != "ff":
                agregar = reemplazar_from_sin_ffd(i[0][1])
                lista_detalle.append(agregar)
                secuencia_nueva.append(lista_detalle)
            #    print("agrego1",lista_detalle)
                lista_detalle = []
            else:
                if i[1][1] in lista_flip_flop_nombres:
                    secuencia_nueva.append(agregar_elemento_a_flip_flop(i[1][1],i[2][1],i[0][1])[0])
                    secuencia_nueva.append(agregar_elemento_a_flip_flop(i[1][1],i[2][1],i[0][1])[1])
                    #print("agrego2",agregar_elemento_a_flip_flop(i[1][1],i[2][1],i[0][1])[0] )
                    lista_detalle = []
                else:
                    generar_flip_flop_combinacional(i[1][1])
                    secuencia_nueva.append(agregar_elemento_a_flip_flop(i[1][1],i[2][1],i[0][1])[0])
                    secuencia_nueva.append(agregar_elemento_a_flip_flop(i[1][1],i[2][1],i[0][1])[1])
                   # print("agrego3",agregar_elemento_a_flip_flop(i[1][1],i[2][1],i[0][1]))
                    lista_detalle = []

        else:
            if i[0][1] in lista_flip_flop_nombres:
               # print("agrego4",agregar_elemento_a_flip_flop(i[0][1], i[1][1], i[2][1]))
                secuencia_nueva.append(agregar_elemento_a_flip_flop(i[0][1], i[1][1], i[2][1]))
                lista_detalle = []
            else:

                generar_flip_flop_combinacional(i[0][1])
                secuencia_nueva.append(agregar_elemento_a_flip_flop(i[0][1], i[1][1], i[2][1]))
               # print("agrego5",agregar_elemento_a_flip_flop(i[0][1], i[1][1], i[2][1]))
                lista_detalle = []

def resultado_a_json(secuencia_nueva):
    lista = []
    for i in secuencia_nueva:
        dict = {}
        for j in i:
            dict[j[0]]=j[1]
        lista.append(dict)

    return lista








setear_not()
setear_or()
setear_and()
reemplazo_secuencia(nuevo)
#print(secuencia_nueva)
#for i in secuencia_nueva:
#    print(i)
secuencia_nueva = (resultado_a_json(secuencia_nueva))
decodifiacion = {"combinational" :secuencia_nueva}
strings = json.dumps(decodifiacion)
#print(strings)
nuevo = json.loads(strings, object_hook=lambda dict_obj: [(key, value) for key, value in dict_obj.items()])

print(nuevo)
