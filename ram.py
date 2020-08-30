class Proceso:
    def __init__(self, id, size):
        self.id = id
        self.size = size
    
    def __str__(self):
        return "id: %s, tamaño %d"%(self.id,self.size)

class DatoLista:
    def __init__(self):
        self.estado = 'H'
        self.posicionI = 0
        self.tamaño = 0
    
    def __str__(self):
        return "|%c|%d|%d|"%(self.estado,self.posicionI,self.tamaño)

class Nodo:
    def __init__(self):
        self.datoL = DatoLista()
        self.siguiente = None

class ListaLibre:
    def __init__(self):
        self.cabeza = None
    
    def mostrar(self):
        if self.cabeza != None:
            actual = self.cabeza
            print(actual.datoL,end="")
            actual = actual.siguiente
            while actual != None:
                print("->",actual.datoL,end="")
                actual = actual.siguiente
        print()

    def generarLista(self,procesos):
        tamaño = 0
        actual = self.cabeza = None
        for i in range(len(procesos)):
            nuevo = Nodo()
            if procesos[i].id == '@':
                nuevo.datoL.estado = 'H'
            else:
                nuevo.datoL.estado = 'P'
            nuevo.datoL.posicionI = tamaño
            nuevo.datoL.tamaño = procesos[i].size
            tamaño += procesos[i].size
            if self.cabeza == None:
                self.cabeza = nuevo
                actual = self.cabeza
            else:
                actual.siguiente = nuevo
                actual = actual.siguiente

def mapaBits(procesos):
    mapa = []
    suma = 0
    for i in range(len(procesos)):
        if procesos[i].id == '@':
            for j in range(procesos[i].size):
                mapa.append(0)
                suma += 1
        else:
            for j in range(procesos[i].size):
                mapa.append(1)
                suma += 1
    for i in range(suma,80,1):
        mapa.append(0)
    for i in range(len(mapa)):
        if i%10 == 0:
            print(" ")
        print(mapa[i],end=" ")
    print("\n")

def agregar(tamaño,procesos):
    if tamaño == 80:
        return tamaño
    while True:
        print("Ingresa identificador del proceso: ", end="")
        id = input()
        bandera = False
        for i in procesos:
            if i.id == id:
                bandera = True    
                break
        if bandera == True:
            print("\tYa hay un porceso con el mismo id")
            print("\t1.-Cambiar de nombre")
            print("\t2.-No crear proceso",end=" ")
            opcion = int(input())
            if opcion == 2:
                return tamaño
        else:
            break
    while True:
        print("Ingresa el tamaño del proceso: ", end="")
        size = int(input())
        if size <= 0:
            print("\tTamaño invalido")
        else:
            break
    if tamaño+size > 80:
        while True:
            print("\tMemoria RAM saturada")
            print("\t1.-Eliminar ultimo proceso (FIFO)")
            print("\t2.-No insertar proceso",end=" ")
            opcion = int(input())
            if opcion == 1:
                #Eliminar ultimo
                return tamaño
            elif opcion == 2:
                return tamaño
            else:
                print("\tOpcion no valida, de otra")
    if len(procesos) == 0:
        procesos.append(Proceso(id,size))
    else:
        bandera = False
        for i in range(len(procesos)):
            if procesos[i].id == '@':
                if procesos[i].size == size:
                    procesos[i].id = id
                    bandera = True
                    break
                elif procesos[i].size > size:
                    procesos[i].id = id
                    procesos.insert(i+1,Proceso('@',procesos[i].size - size))
                    procesos[i].size = size
                    bandera = True
                    break
        if not bandera:
            procesos.append(Proceso(id,size))
    tamaño += size
    return tamaño

if __name__ == '__main__':
    procesos = []
    MAX_SIZE = 80
    actualSize = 0
    lista = ListaLibre()
    while True:
        print(f"\tTamaño ocupado actualmente: {actualSize}")
        print("1.-Insertar proceso")
        print("2.-Eliminar proceso")
        print("3.-Visualizar RAM")
        print("4.-Representacion RAM")
        print("5.-Intercambio de RAM");
        print("6.-Salir", end =" ")
        try:
            opcion = int(input())
        except ValueError as identifier:
            print("Opción no válida\n")
        else:
            if opcion == 1:
                actualSize = agregar(actualSize,procesos)
            elif opcion == 2:
                pass
            elif opcion == 3:
                for i in procesos:
                    print(i)
            elif opcion == 4:
                print("\t1.-Mapa de bits")
                print("\t2.-Listas Libres",end=" ")
                opcion = int(input())
                if opcion == 1:
                    mapaBits(procesos)
                elif opcion == 2:
                    lista.generarLista(procesos)
                    lista.mostrar()
            elif opcion == 5:
                pass
            elif opcion == 6:
                print("\tGracias por usar este programa\n")
                break
            else:
                print("Opción no válida, de otra\n")