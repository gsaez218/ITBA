from datetime import datetime
import os
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from numpy import *


####################################################################################
# FUNCION PARA GESTION DE LAS FECHAS
####################################################################################
def ingresar_fechas():
    # referencia extra usada:   https://parzibyte.me/blog/2020/04/23/validar-fecha-python/
    b_fecha_inicio = 0  # bandeara oara conocer el estado de la fecha inicio ingresada
    b_fecha_fin = 0  # bandeara oara conocer el estado de la fecha fin ingresada
    while b_fecha_inicio == 0:
        try:
            fecha_inicio = input("Ingresa la feha inicio de su consulta en el formato YYYY-MM-DD: ")
            fecha = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            if (fecha <= datetime.today()):  # comprueba que la fecha sea igual o anterior al dia de hoy
                b_fecha_inicio = 1
            else:
                print("la fecha debe ser igual o anterior al día de hoy, reigrésela")
        except ValueError:
            print("Fecha inicial inválida, por favor reingrésela")
            b_fecha_inicio = 0  # si la fecha ingrfesada no es valida, repite el ciclo hasta que este correcta.

    while b_fecha_fin == 0:
        try:
            fecha_fin = input("Ingresa la feha final de su consulta en el formato YYYY-MM-DD: ")
            fecha = datetime.strptime(fecha_fin, '%Y-%m-%d')
            if (fecha <= datetime.today()):  # comprueba que la fecha sea igual o anterior al dia de hoy
                b_fecha_fin = 1
            else:
                print("la fecha debe ser igual o anterior al día de hoy, reigrésela")
        except ValueError:
            print("Fecha final inválida, por favor reingrésela")
            b_fecha_fin = 0  # si la fecha ingrfesada no es valida, repite el ciclo hasta que este correcta.

    if fecha_fin < fecha_inicio:  # verificamos si la fecha final es mayor que la inicial, si no es así las invertimos
        print(
            "Nota: al ser la fecha inicio posterior a la fecha final, se invertirán las mismas para proporcionar el rango correcto de fechas en su consulta")
        fecha_auxiliar = fecha_fin
        fecha_fin = fecha_inicio
        fecha_inicio = fecha_auxiliar

    # print("fecha inicial: ", fecha_inicio)
    # print("fecha final: ", fecha_fin)
    return ([fecha_inicio, fecha_fin])


####################################################################################
# FUNCION CONSULTA API DE FINANZAS
####################################################################################
def consultar_api_finanzas(especie, fecha_inicio, fecha_fin):  # ,fecha_inicio,fecha_fin):
    # Obtenemos la información del mensaje en formato JSON del repositorio consultando la API
    json_file = requests.get(
        f"https://api.polygon.io/v2/aggs/ticker/{especie}/range/1/day/{fecha_inicio}/{fecha_fin}?adjusted=true&sort=asc&limit=120&apiKey=kgNXTHqp5bQH1_H3RcUbUQFk73CB59Z3")
    # print(json_file.text)

    # Longitud en bytes del archivo
    # print(len(json_file.content))

    # Parseamos directamente la respuesta del servidor en formato JSON a un diccionario de Python
    diccionario = json_file.json()

    # El if verifica que existan valores cargados, la variable queryCount nos los dice, ya que si se pide poor ej un sabado y un domingo no hay registros por lo tanto se avisa al usuario
    if diccionario["queryCount"] == 0:
        print("no se encontraron registros para esta consulta")
    else:
        accion = diccionario["ticker"]
        lista_resultados = diccionario["results"]
        # print("Acción elegida = ",accion)
        # aqui recorremos los difernetes valores de la lista y los mostramos (aca se guardan los registros en la BD)

        for indice in lista_resultados:
            # print("Volúmen = ",indice['v'])
            # print("Precio de apertura = ",indice['o'])
            # print("Transacciones = ",indice['n'])
            # print("Menor precio = ",indice['l'])
            # print("Mayor precio = ",indice['h'])

            # le pasamos los argumentos a la función insertar_db para que ella guarda los valores en la tabla de la BD
            insertar_db(
                especie,
                indice['o'],
                indice['n'],
                indice['l'],
                indice['h'],
                fecha_inicio,
                fecha_fin,
                indice['v']
            )
        print("Datos guardados correctamente")


####################################################################################
#             FUNCIONES PARA TRABAJAR CON LA BASE DE DATOS  (SQLite3)              *
####################################################################################

#                         CONSULTAR REGISTRO A LA BASE DE DATOS                    *

def consultar_db():
    # Creamos una conexión con la base de datos
    con = sqlite3.connect('db_finanzas.db')

    # Creamos el curso para interactuar con los datos
    cursor = con.cursor()

    # x = 15
    # Ejecutar comandos de SQL
    res = cursor.execute(f'''
        SELECT *
        FROM registros_API
        ORDER BY especie DESC
    ''')
    #    LIMIT {x};

    for row in res:
        print(row)
    con.close()


#                         INSERTAR REGISTRO A LA BASE DE DATOS                    *

def insertar_db(p_especie, p_precio_apertura, p_transacciones, p_menor_precio, p_mayor_precio, p_fecha_inicio,
                p_fecha_fin, p_volumen):
    # Creamos una conexión con la base de datos
    con = sqlite3.connect('db_finanzas.db')

    # Creamos el curso para interactuar con los datos
    cursor = con.cursor()
    # print(p_especie,p_precio_apertura,p_transacciones,p_menor_precio,p_mayor_precio,p_fecha_inicio,p_fecha_fin,p_volumen)
    # Ejecutar comandos de SQL
    res = cursor.executescript(f'''
           INSERT INTO
           registros_API(especie,precio_apertura,transacciones,menor_precio,mayor_precio,fecha_inicio,fecha_fin,volumen)
            VALUES("{p_especie}", {p_precio_apertura}, {p_transacciones}, {p_menor_precio}, {p_mayor_precio},
           "{p_fecha_inicio}", "{p_fecha_fin}", {p_volumen})
           ;
       ''')
    con.commit()
    con.close()


####################################################################################
#             FUNCION PARA MANEJO DEL MENU     PRINCIPAL                          #
##################################################################################
def menu_principal():
    while True:
        print("*****************************************")
        print("* SISTEMA DE ALTA Y CONSULTA FINANCIERA *")
        print("*****************************************")
        print("MENU PRINCIPAL")
        print("1- Actualización de datos")
        print("2- Visualización de datos")
        print("3. Salir")
        print("\n")
        opcion_menu_principal = input("Elija opción y presione enter: ")
        if opcion_menu_principal == "1":
            menu_opcion_1()
        elif opcion_menu_principal == "2":
            menu_opcion_2()
        elif opcion_menu_principal == "3":
            print("Gracias por usar nuestros servicios")
            break
        else:
            print("Opción incorrecta")


####################################################################################
#             FUNCION PARA MANEJO DEL MENU  CONSULTA API  (Opción  1)             #
##################################################################################
def menu_opcion_1():
    #os.system('cls')
    print("*****************************************")
    print("* SISTEMA DE ALTA Y CONSULTA FINANCIERA *")
    print("*****************************************")
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
        print("*****************************************")
        print("* SISTEMA DE ALTA Y CONSULTA FINANCIERA *")
        print("*****************************************")
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
        elif opcion_menu_visualizacion == "4":
             break
        else:
            print("Opción incorrecta")


####################################################################################
#                     FUNCIONES PARA CONSULTAR bd CON PANDAS                      #
##################################################################################
def consultar_pandas_db():
    con = sqlite3.connect('db_finanzas.db')          # Crea una conexión a la base de datos SQLite
    # Usa read_sql_query de pandas para extraer el resultado de la consulta a un DataFrame
    #pd.options.display.max_rows 60
    pd.options.display.max_columns = None  # imprime todas las columnas disponible si ponemos 5 muestra 5 columnas
    pd.set_option('display.width', 178)    # permite ajustar el ancho para que entren las columnas en pantalla
    df = pd.read_sql_query("SELECT * from registros_API WHERE precio_apertura>= 160 ORDER BY fecha_inicio", con)
    con.close()
    # Verifica que el resultado de la consulta SQL está
    # almacenado en el DataFrame
    # print(df)#.head())
    print(df)
    menor_precio_minimo = df['menor_precio'].min()
    mayor_precio_minimo = df['menor_precio'].max()
    menor_precio_maximo = df['mayor_precio'].min()
    mayor_precio_maximo = df['mayor_precio'].max()
    print(menor_precio_minimo)
    print(mayor_precio_minimo)
    print(menor_precio_maximo)
    print(mayor_precio_maximo)
    apertura = df['precio_apertura']
    apertura.plot(kind='bar')

    ts = pd.Series(random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    fig, ax = plt.subplots(2, 1)
    #ax[0,0]=apertura.plot(kind='bar')
    #ts.plot()
    #apertura.plot()
    plt.show()



####################################################################################
#     FUNCION PARA CONSUTAR bd CON PANDAS DE LOS REGISTRO POR ESPECIE              #
###################################################################################
def consultar_registros_por_especie(p_especie):
    con = sqlite3.connect('db_finanzas.db')  # Crea una conexión a la base de datos SQLite
    # Usa read_sql_query de pandas para extraer el resultado de la consulta a un DataFrame
    pd.options.display.max_rows = None      # imprime todas las filas disponible si ponemos 5 muestra 5 filas
    pd.options.display.max_columns = None  # imprime todas las columnas disponible si ponemos 5 muestra 5 columnas
    pd.set_option('display.width', 178)  # permite ajustar el ancho para que entren las columnas en pantalla
    df = pd.read_sql_query(f"SELECT * from registros_API WHERE especie='{p_especie}' ORDER BY fecha_inicio", con)
    con.close()
    # Verifica que el resultado de la consulta SQL está
    # almacenado en el DataFrame
    # print(df)#.head())
    if len(df)==0:
        print("No se encontraron registros para esa especie")
    else:
        print(df)

####################################################################################
#                     FUNCION PARA CONSULTAR bd CON PANDAS  AGRUPANDO             #
###################################################################################
def consultar_listado_especies():
    con = sqlite3.connect('db_finanzas.db')          # Crea una conexión a la base de datos SQLite

    df = pd.read_sql_query("SELECT * from registros_API", con)
    con.close()
    pd.options.display.max_rows = None  # imprime todas las filas disponible si ponemos 5 muestra 5 filas
    pd.options.display.max_columns = None  # imprime todas las columnas disponible si ponemos 5 muestra 5 columnas
    listado=df.groupby(by=['especie','fecha_inicio','fecha_fin']).mean()
    print(listado.iloc[:, [0, 2]])


