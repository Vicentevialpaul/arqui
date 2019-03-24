import json
import copy
from itertools import product
datos = json.loads(open('example.json').read())
##print(datos)
strings = json.dumps(datos)
nuevo = json.loads(strings, object_hook=lambda dict_obj: [(key, value) for key, value in dict_obj.items()])
for i in nuevo[0][1]:
    pass

circuito_estable = False
output_inicial = None
valor = None
maximo = 0
frecuencia = 0


def quitar_espacios(cadena):
    lista_nueva = []
    for lista in cadena:
        lista_interior = []
        for tupla in lista:
            tupla_nueva = []
            for palabra in tupla:
                try:
                    palabra_nueva = palabra.replace(" ","")
                    tupla_nueva.append(palabra_nueva)
                except:
                    tupla_nueva.append(palabra)
            lista_interior.append(tuple(tupla_nueva))
        lista_nueva.append(lista_interior)
    return lista_nueva

circuito = nuevo[0][1]
delays = nuevo[1][1]
circuito = quitar_espacios(circuito)
delays = quitar_espacios(delays)
##print(delays)

class Simulador:

    def __init__(self):
        self.tiempo = 0
        self.componentes = []
        self.nombre_componentes = []
        self.inputs = []
        self.nombres_inputs = []
        self.out_actual = {}
        self.notificacion = False
        self.tiempo_a_revisar = 0

    def partida(self):
        for componente in self.inputs:
            if componente.nombre[0:5] == "input":
                for i in componente.componentes_a_ir:
                    componente_a_modificar = None
                    for j in self.componentes:
                        if j.nombre == i:
                            #print("desde" + " " + componente.nombre + " valor " + str(componente.valor)
                                 # + " hacia "+ j.nombre)
                            j.entrada_senal(componente.nombre,componente.valor, self.tiempo)


    def actualizar_circuito(self):

        lista_tiempos = []
        for componente in self.componentes:
            lista_a_cambiar = componente.tiempo_proximo_evento
            lista_a_cambiar.sort()
            lista_tiempos.append(lista_a_cambiar[0])
        lista_tiempos.sort()
        self.tiempo = lista_tiempos[0]
        componentes_a_actualizar = []
        for componente in self.componentes:
            if componente.tiempo_proximo_evento[0] == self.tiempo:
                componentes_a_actualizar.append(componente)
        # caso en llegar al mismo tiempo, falta ponerlo
        for componente in componentes_a_actualizar:
            valor_salida = componente.valores_salida[0]
            for i in componente.componentes_a_ir:
                componente_a_modificar = None
                for j in self.componentes:
                    if j.nombre == i:
                        j.entrada_senal(componente.nombre,valor_salida, self.tiempo)
                        #print("desde" + " " + componente.nombre + " valor " + str(valor_salida)
                        #          + " hacia "+ j.nombre)
                if i[0:3] == "out":
                    if self.out_actual[i] != valor_salida:
                        self.out_actual[i] = valor_salida
                    self.notificacion = True
                    #print("out ")
                    #print(self.tiempo)
                    #print(i)
                    #print(valor_salida)
            componente.tiempo_proximo_evento = componente.tiempo_proximo_evento[1:]
            if componente.tiempo_proximo_evento == []:
                componente.tiempo_proximo_evento = [10000000]
            if len(componente.valores_salida) > 1:
              componente.valores_salida = componente.valores_salida[1:]
            #print("fin ciclo")


    def notificacion_m(self):
        if self.notificacion == True:
            self.notificacion = False
            return True
        else:
            return False

    def chequear_salida(self):
        valor = True
        for componente in self.componentes:
            if componente.chequear_salida():
                pass
            else:
                valor = False
        return valor

    def condicion_salida_1(self):   #ademas debe chequear que a todos los componentes le hayan ingresado inputs

        for i in self.componentes:
            lista_a_chequear = i.tiempo_proximo_evento
            lista_a_chequear.sort()
            if lista_a_chequear[0] != 10000000:
                return False
        return True


    def crear_componentes(self,recorrido, lista_delays):
        for lista in recorrido:
            from_a_poner = ""
            gate_a_poner = ""
            to_a_poner = ""
            for tupla in lista:
                ##print(tupla)
                if tupla[0] == "from":
                    from_a_poner = tupla[1]
                if tupla[0] == "gate":
                    gate_a_poner = tupla[1]
                if tupla[0] == "to":
                    to_a_poner = tupla[1]
            if to_a_poner[0:3] == "out":
                if to_a_poner in self.out_actual.keys():
                    pass
                else:
                    self.out_actual[to_a_poner] = 0
            if from_a_poner not in self.nombre_componentes:  #podria ser to tambien..
                ##print("primer if")
                if from_a_poner[0:3] == "ffd":
                   # self.nombres_inputs.append(from_a_poner) ??
                    nuevo_componente = FlipFlop()
                    nuevo_componente.nombre = (from_a_poner)
                    nuevo_componente.componentes_a_ir.append(to_a_poner)
                    for lista in lista_delays:
                        for tupla in lista:
                            if tupla[0] == "gate":
                                nombre = tupla[1]
                            if tupla[0] == "delay":
                                valor = tupla[1]
                        if nombre == from_a_poner:
                            nuevo_componente.delay = valor

                    self.componentes.append(nuevo_componente)
                if from_a_poner[0:3] == "inp":
                    if from_a_poner not in self.nombres_inputs:     #cambios
                     self.nombres_inputs.append(from_a_poner)
                    nuevo_componente = _Input()
                    nuevo_componente.nombre = (from_a_poner)
                    nuevo_componente.componentes_a_ir.append(to_a_poner)
                    for lista in lista_delays:
                        for tupla in lista:
                            if tupla[0] == "gate":
                                nombre = tupla[1]
                            if tupla[0] == "delay":
                                valor = tupla[1]
                        if nombre == from_a_poner:
                            nuevo_componente.delay = valor
                    self.inputs.append(nuevo_componente)
                if from_a_poner[0:3] == "and":
                    self.nombre_componentes.append(from_a_poner)
                    nuevo_componente = _And()
                    nuevo_componente.nombre = (from_a_poner)
                    nuevo_componente.componentes_a_ir.append(to_a_poner)
                    for lista in lista_delays:
                        for tupla in lista:
                            if tupla[0] == "gate":
                                nombre = tupla[1]
                            if tupla[0] == "delay":
                                valor = tupla[1]
                        if nombre == from_a_poner:
                            nuevo_componente.delay = valor
                    self.componentes.append(nuevo_componente)
                if from_a_poner[0:2] == "or":
                    self.nombre_componentes.append(from_a_poner)
                    nuevo_componente = _Or()
                    nuevo_componente.nombre = (from_a_poner)
                    nuevo_componente.componentes_a_ir.append(to_a_poner)
                    for lista in lista_delays:
                        for tupla in lista:
                            if tupla[0] == "gate":
                                nombre = tupla[1]
                            if tupla[0] == "delay":
                                valor = tupla[1]
                        if nombre == from_a_poner:
                            nuevo_componente.delay = valor
                    self.componentes.append(nuevo_componente)
                if from_a_poner[0:3] == "xor":
                    self.nombre_componentes.append(from_a_poner)
                    nuevo_componente = _Xor()
                    nuevo_componente.nombre = (from_a_poner)
                    nuevo_componente.componentes_a_ir.append(to_a_poner)
                    for lista in lista_delays:
                        for tupla in lista:
                            if tupla[0] == "gate":
                                nombre = tupla[1]
                            if tupla[0] == "delay":
                                valor = tupla[1]
                        if nombre == from_a_poner:
                            nuevo_componente.delay = valor
                    self.componentes.append(nuevo_componente)
                if from_a_poner[0:3] == "not":
                    self.nombre_componentes.append(from_a_poner)
                    nuevo_componente = _Not()
                    nuevo_componente.nombre = (from_a_poner)
                    nuevo_componente.componentes_a_ir.append(to_a_poner)
                    for lista in lista_delays:
                        for tupla in lista:
                            if tupla[0] == "gate":
                                nombre = tupla[1]
                            if tupla[0] == "delay":
                                valor = tupla[1]
                        if nombre == from_a_poner:
                            nuevo_componente.delay = valor
                    self.componentes.append(nuevo_componente)
            else:
                componente_a_agregar = None
                for i in self.componentes:
                    if i.nombre == from_a_poner:
                        componente_a_agregar = i
                componente_a_agregar.componentes_a_ir.append(to_a_poner)

class _Input():

    def __init__(self):
        self.valor = 1
        self.nombre = ""
        self.componentes_a_ir = []


# evento, se refiere a cuando se aplica el cambio del valor de algun componente.

### flipflop valor de Q se actualiza alfinal

## INPUT DE C SE ACTUALIZA AL PRINCIPIO
class FlipFlop():

    def __init__(self):
        self.nombre = ""
        self.procedencia_C = None
        self.procedencia_D = None
        self.valor_C = 0
        self.valor_D = 0
        self.componentes_a_ir = []
        self.valores_salida = []
        self.tiempo_proximo_evento = [10000000]
        self.delay = 10
        self.Q = 0
    def chequear_salida(self):
        if self.procedencia_C != None and self.procedencia_D != None:
            return True
    def entrada_senal(self, procedencia, valor, tiempo):

        if tiempo + self.delay in self.tiempo_proximo_evento:
            self.valores_salida.pop()
        else:
            self.tiempo_proximo_evento.append(tiempo + self.delay)

        if procedencia[0:3] == "inp":
            self.procedencia_C = procedencia
            self.valor_C = valor
        else:
            if self.procedencia_D == None:
                self.procedencia_D = procedencia
                self.valor_D = valor
            if self.procedencia_D != None:
                self.valor_D = valor
        self.senal_salida(tiempo)
    def senal_salida(self, tiempo):
        if self.valor_C == 0:
            self.valores_salida.append(self.Q)
        else:
            if self.valor_D == 0:
                self.valores_salida.append(0)
                self.Q = 0
            else:
                self.valores_salida.append(1)
                self.Q = 1




class _And():


    def __init__(self):
        self.nombre = ""
        self.procedencia_1 = None
        self.procedencia_2 = None
        self.valor1 = 0
        self.valor2 = 0
        self.componentes_a_ir = []
        self.valores_salida = []
        self.tiempo_proximo_evento = [10000000]
        self.delay = 10

    def chequear_salida(self):
        if self.procedencia_1 != None and self.procedencia_2 != None:
            return True

    def entrada_senal(self, procedencia, valor, tiempo):
        ##print("procecencia")
        ##print(self.procedencia_1)
        if tiempo + self.delay in self.tiempo_proximo_evento:
            self.valores_salida.pop()
        else:
            self.tiempo_proximo_evento.append(tiempo + self.delay)
        if self.procedencia_1 == None:
            self.procedencia_1 = procedencia
            self.valor1 = valor
        else:
            if self.procedencia_2 == None:
                self.procedencia_2 = procedencia
                self.valor2 = valor
        if self.procedencia_1 != None and self.procedencia_2 != None:
            if self.procedencia_1 == procedencia:
                self.valor1 = valor
            else:
                self.valor2 = valor
        self.senal_salida(None)


    def senal_salida(self, tiempo):
        if self.valor1 ==1 and self.valor2 == 1:
            self.valores_salida.append(1)
        else:
            self.valores_salida.append(0)


class _Or():

    def __init__(self):
        self.nombre = ""
        self.procedencia_1 = None
        self.procedencia_2 = None
        self.valor1 = 0
        self.valor2 = 0
        self.componentes_a_ir = []
        self.valores_salida = []
        self.tiempo_proximo_evento = [10000000]
        self.delay = 10

    def chequear_salida(self):
        if self.procedencia_1 != None and self.procedencia_2 != None:
            return True

    def entrada_senal(self, procedencia, valor, tiempo):
        if tiempo + self.delay in self.tiempo_proximo_evento:
            self.valores_salida.pop()
        else:
            self.tiempo_proximo_evento.append(tiempo + self.delay)
        if self.procedencia_1 == None:
            self.procedencia_1 = procedencia
            self.valor1 = valor
        else:
            if self.procedencia_2 == None:
                self.procedencia_2 = procedencia
                self.valor2 = valor
        if self.procedencia_1 != None and self.procedencia_2 != None:
            if self.procedencia_1 == procedencia:
                self.valor1 = valor
            else:
                self.valor2 = valor
        self.senal_salida()

    def senal_salida(self):
        if self.valor1 ==1 or self.valor2 == 1:
            self.valores_salida.append(1)
        else:
            self.valores_salida.append(0)


class _Xor():

    def __init__(self):
        self.nombre = ""
        self.procedencia_1 = None
        self.procedencia_2 = None
        self.valor1 = 0
        self.valor2 = 0
        self.componentes_a_ir = []
        self.valores_salida = []
        self.tiempo_proximo_evento = [10000000]
        self.delay = 10

    def chequear_salida(self):
        if self.procedencia_1 != None and self.procedencia_2 != None:
            return True

    def entrada_senal(self, procedencia, valor, tiempo):
        ##print("procecencia")
        ##print(self.procedencia_1)
        if tiempo + self.delay in self.tiempo_proximo_evento:
            self.valores_salida.pop()
        else:
            self.tiempo_proximo_evento.append(tiempo + self.delay)
        if self.procedencia_1 == None:
            self.procedencia_1 = procedencia
            self.valor1 = valor
        else:
            if self.procedencia_2 == None:
                self.procedencia_2 = procedencia
                self.valor2 = valor
        if self.procedencia_1 != None and self.procedencia_2 != None:
            if self.procedencia_1 == procedencia:
                self.valor1 = valor
            else:
                self.valor2 = valor
        self.senal_salida()

    def senal_salida(self):
        if self.valor1 ==1 and self.valor2 == 0 or self.valor1 ==0 and self.valor2 == 1:
            self.valores_salida.append(1)
        else:
            self.valores_salida.append(0)


class _Not():

    def __init__(self):
        self.nombre = ""
        self.procedencia_1 = None
        self.valor1 = 0
        self.componentes_a_ir = []
        self.valores_salida = []
        self.tiempo_proximo_evento = [10000000]
        self.delay = 10

    def chequear_salida(self):
        if self.procedencia_1 != None:
            return True

    def entrada_senal(self, procedencia, valor, tiempo):
        ##print("procecencia")
        ##print(self.procedencia_1)
        if tiempo + self.delay in self.tiempo_proximo_evento:
            self.valores_salida.pop()
        else:
            self.tiempo_proximo_evento.append(tiempo + self.delay)
        if self.procedencia_1 == None:
            self.procedencia_1 = procedencia
            self.valor1 = valor
        else:
            self.valor1 = valor
        self.senal_salida()


    def senal_salida(self):
        if self.valor1 ==1:
            self.valores_salida.append(0)
        else:
            self.valores_salida.append(1)


simulador = Simulador()
simulador.crear_componentes(circuito,delays)
simulador.partida()


for i in simulador.componentes:
    pass
    #print(i.delay)
    #print(i.tiempo_proximo_evento)

def chequear_valores_fijos(simulador):
    global circuito_estable
    global valor
    valor = copy.deepcopy(simulador.out_actual)
    output_prueba = copy.deepcopy(simulador.out_actual)
    simulador_prueba = Simulador()
    tiempo = simulador.tiempo
    simulador_prueba.tiempo = tiempo
    #cambiar los componentes
    for i in simulador.componentes:
        if i.nombre[0:3] == "and":
            agregar = _And()
            agregar.nombre = i.nombre
            agregar.procedencia_1 = i.procedencia_1
            agregar.procedencia_2 = i.procedencia_2
            agregar.valor1 = i.valor1
            agregar.valor2 = i.valor2
            agregar.componentes_a_ir = i.componentes_a_ir
            agregar.tiempo_proximo_evento = i.tiempo_proximo_evento
            agregar.valores_salida = i.valores_salida
            agregar.delay = i.delay
            simulador_prueba.componentes.append(agregar)
        if i.nombre[0:3] == "xor":
            agregar = _Xor()
            agregar.nombre = i.nombre
            agregar.procedencia_1 = i.procedencia_1
            agregar.procedencia_2 = i.procedencia_2
            agregar.valor1 = i.valor1
            agregar.valor2 = i.valor2
            agregar.componentes_a_ir = i.componentes_a_ir
            agregar.tiempo_proximo_evento = i.tiempo_proximo_evento
            agregar.valores_salida = i.valores_salida
            agregar.delay = i.delay
            simulador_prueba.componentes.append(agregar)
        if i.nombre[0:2] == "or":
            agregar = _Or()
            agregar.nombre = i.nombre
            agregar.procedencia_1 = i.procedencia_1
            agregar.procedencia_2 = i.procedencia_2
            agregar.valor1 = i.valor1
            agregar.valor2 = i.valor2
            agregar.componentes_a_ir = i.componentes_a_ir
            agregar.tiempo_proximo_evento = i.tiempo_proximo_evento
            agregar.valores_salida = i.valores_salida
            agregar.delay = i.delay
            simulador_prueba.componentes.append(agregar)
        if i.nombre[0:3] == "ffd":
            agregar = FlipFlop()
            agregar.nombre = i.nombre
            agregar.procedencia_C = i.procedencia_C
            agregar.procedencia_D = i.procedencia_D
            agregar.valor_C = i.valor_C
            agregar.valor_D = i.valor_D
            agregar.Q = i.Q
            agregar.componentes_a_ir = i.componentes_a_ir
            agregar.tiempo_proximo_evento = i.tiempo_proximo_evento
            agregar.valores_salida = i.valores_salida
            agregar.delay = i.delay
            simulador_prueba.componentes.append(agregar)
        if i.nombre[0:3] == "not":
            agregar = _Not()
            agregar.nombre = i.nombre
            agregar.procedencia_1 = i.procedencia_1
            agregar.valor1 = i.valor1
            agregar.componentes_a_ir = i.componentes_a_ir
            agregar.tiempo_proximo_evento = i.tiempo_proximo_evento
            agregar.valores_salida = i.valores_salida
            agregar.delay = i.delay
            simulador_prueba.componentes.append(agregar)

    simulador_prueba.nombre_componentes = simulador.nombre_componentes
    simulador_prueba.out_actual = valor
    retorna = "si"
    for i in range(100):
        simulador_prueba.actualizar_circuito()
        if simulador_prueba.out_actual != output_prueba:
            retorna = "no"
    if retorna == "no":
        return False
    else:
        circuito_estable = True
        return True





def simulacion(circuito,delays):

    global circuito_estable
    global maximo
    global frecuencia
    cantidad_simulaciones = 30
    contador = 0
    simulador = Simulador()
    simulador.crear_componentes(circuito,delays)
    cantidad_inputs = len(simulador.nombres_inputs) #cambio
    lista = list(product([0,1], repeat=cantidad_inputs))
    maximo = 0
    for i in lista:
        simulador = Simulador()
        simulador.crear_componentes(circuito,delays)
        for j in range(len(i)):
            for z in simulador.inputs:   ## cambio
                if z.nombre[5:] == str(j+1):
                    z.valor = i[j]
        simulador.partida()
        delay = 0
        print("input")
        print(i)
        for i in simulador.componentes:
            print(i.componentes_a_ir)
        # output por default es 0, se puede chequear si se cambia o no.... sino dejar con output None
        # verificar si en partida se llega a output que no cambia(valor output defecto = 0)

        while True:

            simulador.actualizar_circuito()
            print("tiempo simulador")
            print(simulador.tiempo)
            print("simulador valor")
            print(simulador.out_actual)
            if simulador.notificacion_m():   #cuando se llega a ouput
                #print("not m")
                #print(simulador.out_actual)
                print("tiempo")
                print(simulador.tiempo)
                print("notificacion out actual")
                print(simulador.out_actual)
                if chequear_valores_fijos(simulador):

                    print(" se chequeo valor fijo")
                    print(simulador.tiempo)
                    #print(i)
                    #print("se termina ciclo")
                    #print("valor fijo")
                    print(simulador.tiempo)
                    print(simulador.out_actual)
                    if maximo < simulador.tiempo:
                        maximo = simulador.tiempo
                    #print("break")
                    break
                #print("paso break")
            contador += 1
            #print("contador")
            if cantidad_simulaciones < contador:
                #print("circuito infinito")
                break

             #cambiar de lado
        contador = 0
    if maximo == 0:
        frecuencia = "infinito"
        return ("infinito")
    else:
        frecuencia = 1/maximo
        return 1/maximo






simulacion(circuito,delays)
print("frecuencia maxima")
print(frecuencia)
print("periodo")
print(maximo)
