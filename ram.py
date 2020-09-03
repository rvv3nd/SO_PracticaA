MAX_SIZE = 80
class Proceso:
    def __init__(self, id, size):
        self.id = id
        self.size = size
    
    def __str__(self):
        return "id: %s, tamaño: %d"%(self.id,self.size)

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

def show(procesos,actual):
    if len(procesos) == 0:
        print("\tMemoria vacia")
    else:
        for i in range(len(procesos)):
            print("\t",procesos[i])
        if actual != MAX_SIZE:
            print("\tDisponible",MAX_SIZE - actual)

def agregarElemntos(procesos,tamaño):
    contador = 0
    while True:
        print("Ingresa identificador del proceso: ", end="")
        id = input()
        bandera = False
        for i in procesos:
            if i.id == id:
                bandera = True    
                break
        if bandera:
            print("Ya hay un porceso con el mismo id")
            if contador == 2:
                return tamaño
            print("\t1.-Cambiar de nombre")
            print("\t2.-No crear proceso",end=" ")
            opcion = int(input())
            if opcion == 2:
                return tamaño
        else:
            break
        contador += 1
    contador = 0
    while True:
        print("Ingresa el tamaño del proceso: ", end="")
        try: 
            size = int(input())
        except:
            print("\tTamaño invalido")
            if contador == 2:
                    return tamaño
        else:   
            if size <= 0 or size > MAX_SIZE:
                print("\tTamaño invalido, el rango es (1-80)")
                if contador == 2:
                    return tamaño
            else:
                break
        contador += 1
    contador = 0
    while True:
        if not agregar2(procesos,id,size,tamaño):
            print("\tMemoria RAM saturada")
            show(procesos,tamaño)
            if contador == 3:
                return tamaño
            print("\t1.-Eliminar ultimo proceso (FIFO)")
            print("\t2.-No insertar proceso",end=" ")
            opcion = int(input())
            if opcion == 1:
                tamaño -= borrarProceso(procesos[len(procesos)-1].id,procesos)
            elif opcion == 2:
                return tamaño
            else:
                print("\tOpcion no valida, de otra")
            contador +=1
        else:
            break
    return tamaño + size

def agregar2(procesos,id,size,tamaño):
    if tamaño+size > MAX_SIZE:
        return False
    if len(procesos) == 0:
        procesos.append(Proceso(id,size))
        return True
    bandera = False
    for i in range(len(procesos)):
        if procesos[i].id == '@':
            if procesos[i].size == size:
                procesos[i].id = id
                return True
            elif procesos[i].size > size:
                procesos[i].id = id
                procesos.insert(i+1,Proceso('@',procesos[i].size - size))
                procesos[i].size = size
                return True
    if not bandera:
        casillas = 0
        for i in procesos:
            casillas += i.size
        if casillas+size >MAX_SIZE:
            return False
        procesos.append(Proceso(id,size))
        bandera = True
    return bandera

def borrarProceso(id_to_delet, procesos):
    for i in range(len(procesos)):
        if procesos[i].id == id_to_delet:
            procesos[i].id = '@'
            tam = procesos[i].size
            try:
                if i+1 == len(procesos):
                    if procesos[i-1].id == '@':
                        procesos.pop(i)
                        procesos.pop(i-1)
                    else:
                        procesos.pop(i)
                if procesos[i+1].id == '@':
                    procesos[i].size += procesos[i+1].size
                    procesos.pop(i+1)
                if procesos[i-1].id == '@':
                    procesos[i].size += procesos[i-1].size
                    procesos.pop(i-1)
            except IndexError as noMoreElements:
                return tam
            return tam
    return 0

def fromRAMtoHDD(id_to_move,hdd,procesos,actual):
    for proceso in procesos:
        if proceso.id == id_to_move:
            agregar2(hdd,id_to_move,proceso.size,actual)
            tamaño = proceso.size
            borrarProceso(id_to_move,procesos)
            return tamaño
    return 0

def fromHDDtoRAM(id_to_move,hdd,procesos,actual):
    for proceso in hdd:
        if proceso.id == id_to_move:
            tam = proceso.size
            if agregar2(procesos,id_to_move,proceso.size,actual):
                borrarProceso(id_to_move,hdd)
                return tam
            else:
                print("No hay espacio disponible en RAM")
                return 0
    return 0

def changeSize(procesos,id,actual):
    tam = 0
    for i in range(len(procesos)):
        tam += procesos[i].size
        if procesos[i].id == id:
            value = int(input('Ingresa el valor de incremento o decremento: '))
            if value > 0:
                try:
                    if i+1 == len(procesos) and tam+value <=MAX_SIZE:
                        procesos[i].size += value
                        return value
                    elif procesos[i+1].id == '@': 
                        if procesos[i+1].size == value:
                            procesos.pop(i+1)
                            procesos[i].size += value
                            return value
                        elif procesos[i+1].size > value:
                            procesos[i+1].size -= value
                            procesos[i].size += value
                            return value
                    elif procesos[i-1].id == '@':
                        if procesos[i-1].size == value:
                            procesos.pop(i-1)
                            procesos[i].size += value
                            return value
                        if procesos[i-1].size >= value:
                            procesos[i-1].size -= value
                            procesos[i].size += value
                            return value
                    else:
                        print("Este proceso no puede crecer")
                        return 0
                except IndexError as noMoreElements:
                    return 0         
            elif value < 0:
                if procesos[i].size > -value:
                    try:
                        if i+1 == len(procesos) and i != 0:
                            procesos[i+1].size += -value
                            procesos[i].size += value
                        elif procesos[i+1].id == '@':
                            procesos[i+1].size += -value
                            procesos[i].size += value
                        elif procesos[i-1].id == '@':
                            procesos[i-1].size += -value
                            procesos[i].size += value
                        else:
                            procesos[i].size += value
                            procesos.insert(i+1,Proceso('@',-value))
                    except IndexError as noMoreElements:
                        procesos.insert(i+1,Proceso('@',-value))
                        procesos[i].size += value
                        return 0
                    return value
                else:
                    print("Este proceso no pude decrecer tanto")
                    return 0
            else:
                print('Valor inválido')
    print("No se encontro su id")
    return 0       

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
        print("7.-Ver HDD")
        print("8.-Salir", end =" ")
        try:
            opcion = int(input())
        except ValueError as identifier:
            print("Opción no válida\n")
        else:
            if opcion == 1:
                actualSize = agregarElemntos(procesos,actualSize)
            elif opcion == 2:
                try:
                    id_to_delet = input('Ingresa id a borrar ')
                except ValueError as identifier:
                    print("id invalida")
                else:
                    t = borrarProceso(id_to_delet, procesos)
                    if t > 0 : 
                        print(f"proceso {id_to_delet} eliminado")
                        actualSize -= t
                    else:
                        print(f"No se encontró proceso {id_to_delet}")
            elif opcion == 3:   
                show(procesos,actualSize)
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
                            show(procesos,actualSize)
                            id_to_move = input('Ingresa el ID del proceso a mover a HDD: ')
                            t = fromRAMtoHDD(id_to_move,hdd,procesos,actualSize)
                            if t > 0:
                                print("Proceso movido")
                                actualSize -= t
                            else: 
                                print("No se pudo mover el proceso")
                    elif opc ==2:
                        if len(hdd) == 0:
                            print("El Disco esta vacio. Intente agregar un proceso desde RAM")
                        else:
                            show(hdd,actualSize)
                            id_to_move = input('Ingresa el ID del proceso a mover a RAM: ')
                            t = fromHDDtoRAM(id_to_move,hdd,procesos,actualSize)
                            if t > 0:
                                actualSize += t
                                print("Proceso movido")
                            else:
                                print("No se pudo mover el proceso")
                    else:
                        print("Opcion invalida")
            elif opcion == 6:
                id_to_change = input("Ingresa el ID del proceso: ")
                actualSize += changeSize(procesos,id_to_change,actualSize)
            elif opcion == 7:
                for i in hdd:
                    print(i)
            elif opcion == 8:
                print("\tGracias por usar este programa\n")
                break
            else:
                print("Opción no válida, de otra\n")