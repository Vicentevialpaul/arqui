import json
import sys
import collections
import operator
datos = json.loads(open(sys.argv[1]).read())
#archivo = open(sys.argv[2],"w")
#print(datos)
strings = json.dumps(datos)
#archivo.write(strings)
#print(strings)
nuevo = json.loads(strings, object_hook=lambda dict_obj: [(key, value) for key, value in dict_obj.items()])
#print(datos)
#print(nuevo)
#print([1,2,3])
for i in nuevo[0][1]:
    pass
nuevo = nuevo[0][1]
#print(nuevo)
secuencia_nueva = []
outs = dict()
def agregar_outs(circuito):
    for lista in circuito:
        for elemento in lista:
            if elemento[0] == "to":
                _to = elemento[1]
        if _to[0:3] == "out"  and _to not in outs.keys():
            outs[_to] = []

agregar_outs(nuevo)
def definir_circuito(circuito):
    global outs
    contador = 0
    while True:    # mientras no se hayan agregado todos los elementos
        for lista in circuito:
            if len(lista) == 2:     # caso donde no hay flip flop
                _from = lista[0][1]
                _to = lista[1][1]
            if len(lista) == 3:
                _from = None
                _to = None
                for i in lista:
                    if i[0] == "from":
                        _from = i[1]
                    if i[0] == "to":
                        _to = i[1]
            if _to[0:3] == "out":  # caso que venga de un out
                if [_from,_to] not in outs[_to]:
                    contador += 1
                    outs[_to] = [[_from,_to]] + outs[_to]
            else:   # si no viene de out , se revisa si viene de algun elemento en lista de out
                for out in outs:
                    secuencia = outs[out]
                    if [_from,_to] not in secuencia:
                        lista_to = [i[0] for i in secuencia]
                        lista_from = [i[1] for i in secuencia]
                        if _to in lista_to and _from not in lista_from:
                            contador += 1
                            outs[out] = [[_from,_to]] + outs[out]
                        elif _to in lista_to and _from in lista_from:  #ciclo
                            indice = lista_to.index(_to)
                            outs[out] = outs[out][0:indice]+ [[_from,_to]] + outs[out][indice:]
                            contador += 1
        if contador >= len(circuito):
            break
definir_circuito(nuevo)

def establecer_circuito(outs):  # le llega outs
    global nuevo
    lista_final = []
    for out in outs:
        secuencia = outs[out]
        secuencia.reverse()
        termino = "no"
        for lista in secuencia:
            if lista[0][0:3] == "ffd" and termino == "no": ## al llegar a un flipflop desde el output, revisar condicio
                                                            #nes y agregar a lista final circuito desde out a flipflop
                indice = secuencia.index(lista)
                lista_final = secuencia[0:indice + 1]
                if secuencia[indice+1][1] == secuencia[indice][1]:
                    # si es que objeto tiene dos llegadas, seguir recorriendo circuito
                    pass
                else:
                    termino = "si"
        if termino == "no":
            lista_final = lista_final + outs[out]
    lista_nueva = []
    for i in lista_final:   # eliminar inputs
        #print(i)
        if "input" in i[0]:
            pass
        else:
            lista_nueva.append(i)
    return lista_nueva

secuencia_nueva = establecer_circuito(outs)
def resultado_a_json(secuencia_nueva):
    lista = []
    for i in secuencia_nueva:
        dict = collections.OrderedDict()
        dict["from"] = i[0]
        dict["to"] = i[1]
        lista.append(dict)

    return lista
secuencia_nueva = (resultado_a_json(secuencia_nueva))
decodifiacion = {"output" :secuencia_nueva}
strings = json.dumps(decodifiacion)
nuevo = json.loads(strings, object_hook=lambda dict_obj: [(key, value) for key, value in dict_obj.items()])
with open(sys.argv[2], 'w') as file:
    json.dump(decodifiacion, file)






