class Proceso:

    def __init__(self, id, size):
        self.id = id
        self.size = size


if __name__ == '__main__':
    
    procesos = []
    MAX_SIZE = 80
    actualSize = 0
    while True:
        print(f"Tamaño ocupado actualmente: {actualSize}")
        print("1.-Crear proceso\n")
        print("2.-Eliminar proceso\n")
        print("3.-Visualizar RAM\n")
        print("4.-Salir\n")
        try:
            opcion = int(input('Ingrese opción deseada: '))
        except ValueError as identifier:
            print("Opción no válida\n")
        else:
            if opcion == 1:
                id = input('\nIngresa identificador del proceso: ')
                try: 
                    size = int(input('\nIngresa el tamaño del proceso: '))
                except ValueError as identifier:
                    print("Tamaño no válido\nCreación de proceso abortada\n")
                else:
                    proceso = Proceso(id,size)
                    procesos.append(proceso)
                    actualSize += size
            elif opcion == 2:
                toDelet = int(input('Ingresa el ID del proceso a borrar'))
            elif opcion == 3:
                pass
            elif opcion == 4:
                break
            else:
                print("Opción no válida\n")


