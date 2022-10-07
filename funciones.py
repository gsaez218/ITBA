from datetime import datetime
import os
import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
#from numpy import *
import numpy as np

####################################################################################
#                       FUNCION PARA GESTION DE LAS FECHAS                         #
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
#                       FUNCION CONSULTA API DE FINANZAS                           #
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
#             FUNCIONES PARA TRABAJAR CON LA BASE DE DATOS  (SQLite3)              #
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
#     FUNCION PARA ELIMINACION DE REGISTROS DE LA BD (TODOS)                       #
####################################################################################
def eliminar_registros_bd():
   con = sqlite3.connect('db_finanzas.db')           # Creamos una conexión con la base de datos
   cursor = con.cursor()                             # Creamos el curso para interactuar con los datos
   res = cursor.execute(f'''                         
        DELETE 
        FROM registros_API
        ''')
   con.commit()
   con.close()
   print("se eliminaron TODOS los registros de la BD")


####################################################################################
#     FUNCION PARA ELIMINACION DE REGISTROS DE LA BD (X ESPECIE)                   #
####################################################################################
def eliminar_especie_bd(p_especie):
    con = sqlite3.connect('db_finanzas.db')  # Creamos una conexión con la base de datos
    cursor = con.cursor()  # Creamos el curso para interactuar con los datos
    res = cursor.execute(f'''
           SELECT *
           FROM registros_API
           WHERE especie="{p_especie}"
    ''')
    cantidad_registros=(len(cursor.fetchall()))   # vemos cuantos registros devuelve  la consulta SQL
    if cantidad_registros==0:
        print("No se encontraron registros para la especie elegida")
    else:
        res = cursor.execute(f'''                         
             DELETE 
             FROM registros_API
             WHERE especie="{p_especie}"
        ''')
        print("se eliminaron ",cantidad_registros," registros de la BD correspondeinte a la especie ", p_especie)
    con.commit()
    con.close()


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
#                     FUNCION PARA CONSULTAR bd CON PANDAS  AGRUPANDO              #
####################################################################################
def consultar_listado_especies():
    con = sqlite3.connect('db_finanzas.db')          # Crea una conexión a la base de datos SQLite

    df = pd.read_sql_query("SELECT * from registros_API", con)
    con.close()
    pd.options.display.max_rows = None  # imprime todas las filas disponible si ponemos 5 muestra 5 filas
    pd.options.display.max_columns = None  # imprime todas las columnas disponible si ponemos 5 muestra 5 columnas
    listado=df.groupby(by=['especie','fecha_inicio','fecha_fin']).mean()
    print(listado.iloc[:, [0, 2]])


####################################################################################
#                     FUNCIONES PARA CONSULTAR bd CON PANDAS                       #
####################################################################################
def consultar_pandas_db():
    p_especie = input("Ingrese la especie financiera a consultar: ")
    #fechas = ingresar_fechas()
    con = sqlite3.connect('db_finanzas.db')          # Crea una conexión a la base de datos SQLite
    # Usa read_sql_query de pandas para extraer el resultado de la consulta a un DataFrame
    #pd.options.display.max_rows 60
    pd.options.display.max_columns = None  # imprime todas las columnas disponible si ponemos 5 muestra 5 columnas
    pd.set_option('display.width', 178)    # permite ajustar el ancho para que entren las columnas en pantalla
    #df = pd.read_sql_query("SELECT * from registros_API WHERE precio_apertura>= 160 ORDER BY fecha_inicio", con)
    df = pd.read_sql_query(
        f"SELECT * from registros_API WHERE especie='{p_especie}' ORDER BY fecha_inicio",
        con)
    con.close()

    """
    print(df)
    print("Menor precio \n", df['menor_precio'])
    print(df.index)
    menor_precio_minimo = df['menor_precio'].min()
    mayor_precio_minimo = df['menor_precio'].max()
    menor_precio_maximo = df['mayor_precio'].min()
    mayor_precio_maximo = df['mayor_precio'].max()
    print(menor_precio_minimo)
    print(mayor_precio_minimo)
    print(menor_precio_maximo)
    print(mayor_precio_maximo)
"""

    t=(df.index)
    apertura=(df['precio_apertura'])
    menor_p=(df['menor_precio'])
    mayor_p=(df['mayor_precio'])
    fig, axs = plt.subplots(2, 1)
    plt.title('Pedidos de postres')
    axs[0].plot(t, apertura, t, menor_p, t, mayor_p)
    axs[0].set_xlim(0, df.index.max())
   # axs[0].set_xlabel('Evolución de los registros')
    axs[0].set_ylabel('Precios    [U$s]')
    axs[0].grid(True)
    axs[0].legend(['Precio apertura', 'Menor precio', 'Mayor precio'], loc=0)

    transacciones = (df['transacciones'])
    axs[1].plot(t, transacciones)
    axs[1].set_xlim(0, df.index.max())
    axs[1].set_xlabel('Evolución de los registros')
    axs[1].set_ylabel('Transacciones    [millones]')
    axs[1].grid(True)

    plt.show()
    plt.close('all')


"""

    fig, ax = plt.subplots()
    x_values = (df.index)
    y_values = (df['transacciones'])
    plt.bar(x_values, y_values)


   # apertura = df['precio_apertura']
    #apertura.plot(kind='bar')

    #########################################################################

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    dt = 0.01
    t = np.arange(0, 30, dt)
    nse1 = np.random.randn(len(t))  # white noise 1
    nse2 = np.random.randn(len(t))  # white noise 2

    # Two signals with a coherent part at 10Hz and a random part
    s1 = np.sin(2 * np.pi * 10 * t) + nse1
    s2 = np.sin(2 * np.pi * 10 * t) + nse2



    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, s1, t, s2)
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    cxy, f = axs[1].cohere(s1, s2, 256, 1. / dt)
    axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()

#########################################################################

    #plt.show()
"""