import csv
import os

def menu_usuario():
    ARCHIVO_VIATICOS = "viaticos.csv"
    CAMPOS = ['Legajo', 'Apellido', 'Nombre']

    while True:
        print("Ingrese una opción: \n1- Cargar y guardar datos. \n2- Calcular gastos. \n3- Salir.")
        opcion = input("")
        if opcion == "1":
            cargar_datos(CAMPOS)
        if opcion == "2":
            calculo_viaticos(ARCHIVO_VIATICOS, CAMPOS)
        if opcion == "3":
            exit()

def cargar_datos(campos):
    guardar = "si"
    lista_empleados = []
    nombre_archivo = input("Ingrese el nombre del archivo (no hace falta agregar la extension .csv): ")
    nombre_archivo_csv = nombre_archivo + ".csv"

    while guardar == "si":
        empleado = {}
        for campo in campos:
            valorCampo = input(f"Ingrese {campo} del empleado: ")
            if campo == campos[0]:
                resultado = validar_numero(valorCampo)
                empleado[campo] = resultado
            else:
                empleado[campo] = valorCampo
        lista_empleados.append(empleado)
        guardar = input("Desea agregar otro empleados? Si/No ")

    try:
        archivo_existe = os.path.isfile(nombre_archivo_csv)
        if archivo_existe:
            opcion_doc = input("El archivo ya existe, que quiere hacer? \n1- Sobreescribir \n2- Modificar \n")
            if opcion_doc == "1":
                manejo_archivos('w', nombre_archivo_csv, campos, lista_empleados)
                print("El archivo se sobreescribio con exito")
            elif opcion_doc == "2":
                manejo_archivos('a', nombre_archivo_csv, campos, lista_empleados)
                print("El archivo se modificó con exito")
        else:
            manejo_archivos('w', nombre_archivo_csv, campos, lista_empleados)
            print("El archivo se creo con exito.")
        menu_usuario()
    except IOError:
        print("Error al abrir el archivo")

def calculo_viaticos(viaticos, campos):
    total_gastos = 0
    MONTO_MAXIMO = 5000

    while True:
        opcion = input("Necesita un archivo csv con datos de empleados, seleccione una opción:\n"
                       "1- Cargar informacion desde un archivo existente.\n"
                       "2- Guardar información y crear un archivo nuevo.\n")
        if opcion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo (no hace falta agregar la extension .csv):\n")
            nombre_archivo_csv = nombre_archivo + ".csv"
            try:
                with open(nombre_archivo_csv, 'r', newline='') as a_legajos, open(viaticos, 'r', newline='') as a_viaticos:
                    numero_legajo = validar_numero(input("Ingresa un número de legajo:\n"))
                    legajos_csv = csv.reader(a_legajos)
                    viaticos_csv = csv.reader(a_viaticos)
                    next(legajos_csv)
                    next(viaticos_csv)
                    legajos = next(legajos_csv, None)
                    gastos_viaticos = next(viaticos_csv, None)

                    while legajos:
                        while gastos_viaticos:
                            if int(gastos_viaticos[0]) == numero_legajo:
                                total_gastos += int(gastos_viaticos[1])
                            gastos_viaticos = next(viaticos_csv, None)
                        if int(legajos[0]) == numero_legajo:
                            if total_gastos > MONTO_MAXIMO:
                                deuda = total_gastos - MONTO_MAXIMO
                                print(f"Legajo {legajos[0]}: {legajos[2]} {legajos[1]} gasto {total_gastos} y se ha "
                                      f"pasado del presupuesto por {deuda}")
                            else:
                                print(f"Legajo {legajos[0]}: {legajos[2]} {legajos[1]} gastó {total_gastos}")
                            menu_usuario()
                        legajos = next(legajos_csv, None)
                    print(f"El legajo {numero_legajo} es inválido, volve a intentarlo.")
            except IOError:
                print("Error al abrir el archivo, volvé a intentarlo.")
        if opcion == "2":
            cargar_datos(campos)

# Funcion para validar que un input sea un número
def validar_numero(numero):
    try:
        return int(numero)
    except ValueError:
        return validar_numero(input("El valor ingresado no es valido, ingresa otro numero:\n"))

# Funcion para modificar o crear un archivo
def manejo_archivos(accion, archivo_csv, campos, lista):
    with open(archivo_csv, accion, newline='') as file:
        file_guarda = csv.DictWriter(file, fieldnames=campos)
        if accion == 'w':
            file_guarda.writeheader()
        file_guarda.writerows(lista)
    return

menu_usuario()
