from funciones import *

####################################################################################
#             FUNCION PARA MANEJO DEL MENU     PRINCIPAL                          #
##################################################################################
def menu_principal():
    while True:
        print("***********************************************")
        print("* SISTEMA DE ALTA, BAJA Y CONSULTA FINANCIERA *")
        print("***********************************************")
        print("MENU PRINCIPAL")
        print("1- Actualización de datos")
        print("2- Visualización de datos")
        print("3- Eliminación de datos")
        print("4- Salir")
        print("\n")
        opcion_menu_principal = input("Elija opción y presione enter: ")
        if opcion_menu_principal == "1":
            menu_opcion_1()
        elif opcion_menu_principal == "2":
            menu_opcion_2()
        elif opcion_menu_principal == "3":
            menu_opcion_3()
        elif opcion_menu_principal == "4":
            print("Gracias por usar nuestros servicios")
            break
        else:
            print("Opción incorrecta")


####################################################################################
#             FUNCION PARA MANEJO DEL MENU  CONSULTA API  (Opción  1)             #
##################################################################################
def menu_opcion_1():
    #os.system('cls')
    print("***********************************************")
    print("* SISTEMA DE ALTA, BAJA Y CONSULTA FINANCIERA *")
    print("***********************************************")
    print("MENU - Actualización de datos \n ")
    especie = input("Ingrese la especie financiera a consultar: ")
    fechas = ingresar_fechas()
    print("Pidiendo datos...")
    consultar_api_finanzas(especie, fechas[0], fechas[1])


####################################################################################
#             FUNCION PARA MANEJO MENU VISUALIZACION      (Opción  2)             #
##################################################################################
def menu_opcion_2():
    while True:
        print("***********************************************")
        print("* SISTEMA DE ALTA, BAJA Y CONSULTA FINANCIERA *")
        print("***********************************************")
        print("MENU - Visualización de datos \n ")
        print("1- Listado de registros por especie")
        print("2- Listado de grupos de especies ordenados por fechas")
        print("3- Gráfico de barras de una especie por rango de fechas")
        print("4. Regresar al Menú Principal")
        print("\n")
        opcion_menu_visualizacion = input("Elija opción y presione enter: ")
        if opcion_menu_visualizacion == "1":
            especie = input("Ingrese especice a consultar")
            consultar_registros_por_especie(especie)
        elif opcion_menu_visualizacion == "2":
            print("Los tickers guardados en la base de datos son:")
            consultar_listado_especies()
        elif opcion_menu_visualizacion == "3":
            print("Grafico por especie")
            consultar_pandas_db()
        elif opcion_menu_visualizacion == "4":
             break
        else:
            print("Opción incorrecta")


####################################################################################
#     FUNCION PARA MANEJO ELIMINACION DE REGISTROS DE LA BD      (Opción  3)      #
##################################################################################
def menu_opcion_3():
    while True:
        print("***********************************************")
        print("* SISTEMA DE ALTA, BAJA Y CONSULTA FINANCIERA *")
        print("***********************************************")
        print("MENU - Eliminación de registros de la BD \n ")
        print("1- Eliminar TODOS los registros de la BD")
        print("2- Eliminar registros por especie")
        print("3- Regresar al Menú Principal")
        print("\n")
        opcion_menu_visualizacion = input("Elija opción y presione enter: ")
        if opcion_menu_visualizacion == "1":
            eliminar_registros_bd()
        elif opcion_menu_visualizacion == "2":
            p_especie = input("Ingrese la especia a eliminar de la BD: ")
            eliminar_especie_bd(p_especie)
        elif opcion_menu_visualizacion == "3":
             break
        else:
            print("Opción incorrecta")