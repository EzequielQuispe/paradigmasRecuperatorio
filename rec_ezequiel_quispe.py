import csv
import os

def menu_usuario():
    CAMPOS = ['Legajo', 'Apellido', 'Nombre']
    ARCHIVO_VIATICOS = "viaticos.csv"
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
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    while guardar == "si":
        empleado = {}
        for campo in campos:
            valorCampo = input(f"Ingrese {campo} del empleado: ")
            empleado[campo] = valorCampo
        lista_empleados.append(empleado)
        guardar = input("Desea agregar otro empleados? Si/No ")
    try:
        archivo_existe = os.path.isfile(nombre_archivo)
        if archivo_existe:
            opcion_doc = input("El archivo ya existe, que quiere hacer? \n1- Sobreescribir \n2- Modificar \n")
            if opcion_doc == "1":
                with open(nombre_archivo, 'w', newline='') as file:
                    file_guarda = csv.DictWriter(file, fieldnames=campos)
                    file_guarda.writeheader()
                    file_guarda.writerows(lista_empleados)
            elif opcion_doc == "2":
                with open(nombre_archivo, 'a', newline='') as file:
                    file_guarda = csv.DictWriter(file, fieldnames=campos)
                    file_guarda.writerows(lista_empleados)
        else:
            with open(nombre_archivo, 'w+', newline='') as file:
                file_guarda = csv.DictWriter(file, fieldnames=campos)
                file_guarda.writeheader()
                file_guarda.writerows(lista_empleados)
        menu_usuario()
    except IOError:
        print("Error al abrir el archivo")

def calculo_viaticos(viaticos, empleados):
    total_gastos = 0
    MONTO_MAXIMO = 5000
    while True:
        opcion = input("Seleccione una opción:\n1- Cargar informacion desde un archivo existente.\n"
                       "2- Guardar información y crear un archivo nuevo.\n")
        if opcion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo:\n")
            nombre_archivo_csv = nombre_archivo + ".csv"
            try:
                with open(nombre_archivo_csv, 'r', newline='') as a_legajos, open(viaticos, 'r', newline='') as a_viaticos:
                    numero_legajo = input("Ingresa un número de legajo:\n")
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
                                print(f"Legajo {legajos[0]}: {legajos[2]} {legajos[1]} debe {deuda}")
                            else:
                                print(
                                    f"Legajo {legajos[0]}: {legajos[2]} {legajos[1]} gastó {total_gastos} en viaticos")
                            menu_usuario()
                        legajos = next(legajos_csv, None)
                    print(f"El legajo {numero_legajo} es inválido, volve a intentarlo.")
            except IOError:
                print("Error al abrir el archivo, volvé a intentarlo.")
        if opcion == "2":
            cargar_datos(empleados)

menu_usuario()
