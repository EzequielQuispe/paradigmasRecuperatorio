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
    monto_maximo = 5000
    while True:
        opcion = input("Seleccione una opción:\n"
                       "1- Cargar informacion desde un archivo existente.\n"
                       "2- Guardar información y crear un archivo nuevo.\n")
        if opcion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo:\n")
        if opcion == "2":
            cargar_datos(empleados)

menu_usuario()
