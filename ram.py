MAX_SIZE = 80
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
    for i in range(suma,MAX_SIZE,1):
        mapa.append(0)
    for i in range(len(mapa)):
        if i%10 == 0:
            print(" ")
        print(mapa[i],end=" ")
    print("\n")

def agregar(tamaño,procesos):
    if tamaño == MAX_SIZE:
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
        try: 
            size = int(input())
        except:
            print("\tTamaño invalido")
        else:   
            if size <= 0:
                print("\tTamaño invalido")
            else:
                break
    if tamaño+size > MAX_SIZE:
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

def borrarProceso(id_to_delet, procesos):
    for proceso in procesos:
        if proceso.id == id_to_delet:
            proceso.id = '@'
            return proceso.size
    return 0

def fromRAMtoHDD(id_to_move,hdd,procesos):
    for proceso in procesos:
        if proceso.id == id_to_move:
            hdd.append(Proceso(id_to_move,proceso.size))
            proceso.id = '@'
            return proceso.size
    return 0

def fromHDDtoRAM(id_to_move,hdd,procesos,actual):
    for proceso in hdd:
        if proceso.id == id_to_move:
            if proceso.size + actual < 80:
                procesos.append(proceso)
                hdd.remove(proceso)
                return proceso.size
            else:
                print("No hay espacio disponible en RAM")
                return 0
    return 0

def changeSize(procesos,id,actual):
    for i in range(len(procesos)):
        if procesos[i].id == id:
            value = int(input('Ingresa el valor de incremento o decremento: '))
            if value > 0:
                try:
                    if procesos[i+1].id == '@':
                        if actual + value < MAX_SIZE:      
                            procesos[i+1].size -= value
                            procesos[i].size += value
                    else:
                        print("Este proceso no puede crecer")
                except IndexError as noMoreElements:
                    if actual + value < MAX_SIZE:
                        procesos[i].size += value
                return value         
            elif value < 0:
                if procesos[i].size > -1*value:
                    procesos[i].size += value
                    return 0
                else:
                    print("Este proceso no pude decrecer tanto")
            else:
                print('Valor inválido')
    return 0           
def show(procesos):
    for i in procesos:
        print(i)

if __name__ == '__main__':
    procesos = []
    hdd = []
    actualSize = 0
    lista = ListaLibre()
    while True:
        print(f"\tTamaño ocupado actualmente: {actualSize}")
        print("1.-Insertar proceso")
        print("2.-Eliminar proceso")
        print("3.-Visualizar RAM")
        print("4.-Representacion RAM")
        print("5.-Intercambio de RAM")
        print("6.-Cambiar tamaño de proceso")
        print("7.-Salir", end =" ")
        try:
            opcion = int(input())
        except ValueError as identifier:
            print("Opción no válida\n")
        else:
            if opcion == 1:
                actualSize = agregar(actualSize,procesos)
            elif opcion == 2:
                try:
                    id_to_delet = input('Ingresa id a borrar')
                except ValueError as identifier:
                    print("id invalida")
                else:
                    t = borrarProceso(id_to_delet, procesos)
                    if t > 0 : 
                        print(f"proceso {id_to_delet} eliminado\n")
                        actualSize -= t
                    else:
                        print(f"No se encontró proceso {id_to_delet}\n")
            elif opcion == 3:   
                show(procesos)
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
                print("\t1.-Pasar proceso de RAM a HDD")
                print("\t2.-Pasar proceso de HDD a RAM")
                try:
                    opc =  int(input('Opcion deseada: '))
                except ValueError as e:
                    print("Opcion invalida")
                else:
                    if opc == 1:
                        if len(procesos) == 0 :
                            print("Memoria RAM sin procesos")
                        else:
                            show(procesos)
                            id_to_move = input('Ingresa el ID del proceso a mover a HDD: ')
                            t = fromRAMtoHDD(id_to_move,hdd,procesos)
                            if t > 0:
                                print("Proceso movido")
                            else: 
                                print("No se pudo mover el proceso")
                    elif opc ==2:
                        if len(hdd) == 0:
                            print("El Disco esta vacio. Intente agregar un proceso desde RAM")
                        else:
                            show(hdd)
                            id_to_move = input('Ingresa el ID del proceso a mover a RAM: ')
                            t = fromHDDtoRAM(id_to_move,hdd,procesos,actualSize)
                            if t > 0:
                                actualSize += t
                                print("Proceso movido")
                            else:
                                print("No se pudo mover el proceso")
                    else:
                        print("Opcion invalida")
            elif opcion ==6:
                id_to_change = input("Ingresa el ID del proceso: ")
                actualSize += changeSize(procesos,id_to_change,actualSize)
            elif opcion == 7:
                print("\tGracias por usar este programa\n")
                break
            else:
                print("Opción no válida, de otra\n")