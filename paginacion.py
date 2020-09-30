MAX_SIZE = 0

class Proceso:
    def __init__(self, id, size):
        self.id = id
        self.size = size
    
    def __str__(self):
        return "id: %s, tamaño: %d"%(self.id,self.size)

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
            print("\t1.-Cambiar de identificador")
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
    if not agregar2(procesos,id,size,tamaño):
        print("\tMemoria RAM saturada")
    else:
        print("\tSe agrego el proceso")
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

if __name__ == '__main__':
    MAX_SIZE = int(input('Max de memoria: '))
    porcion = int(input("Porcentaje para cada página: "))
    size_per_page = int(MAX_SIZE * (porcion/100))
    procesos = []
    actualSize = 0
    while True:
        print('1.-Insertar proceso')
        print('2.-Eliminar proceso')
        print('3.-Ver Ram')
        print('4.-Salir')
        try:
            opc = int(input())
        except ValueError as identifier:
            print(f'Error {identifier}')
        else:
            if opc == 1:
                actualSize = agregarElemntos(procesos,actualSize)
            elif opc == 2:
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
            elif opc == 3:
                if len(procesos) == 0:
                    print("Memoria vacia")
                    continue
                else:
                    i = 0
                    max = 0
                    pag = 1
                    for proceso in procesos:
                        tam = proceso.size
                        for j in range(tam):
                            if i == size_per_page:
                                print("Pagina ",pag)
                                i = 0
                                pag += 1
                            print(f"[{proceso.id}]",end=" ")
                            i += 1
                            max +=1
                    while max != MAX_SIZE:
                        if i == size_per_page:
                            print("Pagina ",pag)
                            i = 0
                            pag += 1
                        print("[@]",end=" ")
                        i += 1
                        max +=1
                    print("Pagina ",pag)
                print()
            elif opc == 4:
                print("Gracias por usar este programa")
                break
            else:
                print('Opción no válida')