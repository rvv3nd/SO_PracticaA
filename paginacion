class Proceso:
    def __init__(self, id, size):
        self.id = id
        self.size = size
    
    def __str__(self):
        return "id: %s, tamaño: %d"%(self.id,self.size)

def existe(name,procesos):
    for proceso in procesos:
        if name == proceso.id: return proceso
    return None


if __name__ == "__main__":
    
    MAX = int(input('Max de memoria: '))
    porcion = int(input("Porcentaje para cada página: "))

    size_per_page = int(MAX * (porcion/100))
    actual_size = 0

    procesos = []
    libro = []
    pagina = []
    print(size_per_page)
    while True:
        print('1.-Insertar proceso')
        print('2.-Ver paginas')
        print('3.-Eliminar proceso')
        print('4.-Salir')
        try:
            opc = int(input("Opción deseada: "))
        except Exception as e:
            print(f'Error {e}')
        else:
            if opc == 1:
                print (f'Memoria usada: {actual_size}')
                name = input('Identificador de proceso: ')
                size = int(input('Tamaño del proceso: '))
                if existe(name,procesos) == None and actual_size+size <= MAX:
                    proceso = Proceso(name,size)
                    procesos.append(proceso)
                    actual_size += size
                else:
                    print('Error. Proceso existente o memoria excedida. Intente de nuevo')
            elif opc == 2:
                num_hoja = 0
                pagina.clear()
                for proceso in procesos:
                    temp = proceso.size
                    while temp > 0:
                        if len(pagina) < size_per_page:
                            pagina.append(proceso.id)
                            temp -= 1
                        else: #osease que ya se llenó la pagina
                            print(f'Hoja {num_hoja}')
                            print(pagina)
                            pagina.clear()
                            num_hoja +=1
                print(f'Hoja {num_hoja}')
                print(pagina)
            elif opc == 3:
                name = input('ID del proceso a borrar: ')
                proceso = existe(name,procesos)
                if not proceso == None:
                    procesos.remove(proceso)
                    print(f'Proceso {name} eliminado')
                else:
                    print('No existe tal proceso')
            elif opc == 4:
                break
            else:
                print('Opción no válida')
