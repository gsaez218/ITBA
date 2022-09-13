from datetime import datetime
import requests
import sqlite3


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
            if (fecha<=datetime.today()):       # comprueba que la fecha sea igual o anterior al dia de hoy
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
            if (fecha<=datetime.today()):       # comprueba que la fecha sea igual o anterior al dia de hoy
                b_fecha_fin = 1
            else:
                print("la fecha debe ser igual o anterior al día de hoy, reigrésela")
        except ValueError:
            print("Fecha final inválida, por favor reingrésela")
            b_fecha_fin = 0  # si la fecha ingrfesada no es valida, repite el ciclo hasta que este correcta.

    if fecha_fin < fecha_inicio:  # verificamos si la fecha final es mayor que la inicial, si no es así las invertimos
        print("Nota: al ser la fecha inicio posterior a la fecha final, se invertirán las mismas para proporcionar el rango correcto de fechas en su consulta")
        fecha_auxiliar = fecha_fin
        fecha_fin = fecha_inicio
        fecha_inicio = fecha_auxiliar

    #print("fecha inicial: ", fecha_inicio)
    #print("fecha final: ", fecha_fin)
    return([fecha_inicio,fecha_fin])


####################################################################################
# FUNCION CONSULTA API DE FINANZAS
####################################################################################
def consultar_api_finanzas(especie,fecha_inicio,fecha_fin):#,fecha_inicio,fecha_fin):
    # Obtenemos la información del mensaje en formato JSON del repositorio consultando la API
    json_file = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{especie}/range/1/day/{fecha_inicio}/{fecha_fin}?adjusted=true&sort=asc&limit=120&apiKey=kgNXTHqp5bQH1_H3RcUbUQFk73CB59Z3")
    print(json_file.text)

    # Longitud en bytes del archivo
    #print(len(json_file.content))

    # Parseamos directamente la respuesta del servidor en formato JSON a un diccionario de Python
    diccionario = json_file.json()

    # El if verifica que existan valores cargados, la variable queryCount nos los dice, ya que si se pide poor ej un sabado y un domingo no hay registros por lo tanto se avisa al usuario
    if diccionario["queryCount"]==0:
        print("no se registraron valores para ese rango de fechas")
    else:
        accion = diccionario["ticker"]
        lista_resultados = diccionario["results"]
        print("Acción elegida = ",accion)
        #aqui recorremos los difernetes valores de la lista y los mostramos (aca se guardan los registros en la BD)

        for indice in lista_resultados:
            #print("Volúmen = ",indice['v'])
            #print("Precio de apertura = ",indice['o'])
            #print("Transacciones = ",indice['n'])
            #print("Menor precio = ",indice['l'])
            #print("Mayor precio = ",indice['h'])

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

####################################################################################
#             FUNCIONES PARA TRABAJAR CON LA BASE DE DATOS  (SQLite3)              *
####################################################################################

#                         CONSULTAR REGISTRO A LA BASE DE DATOS                    *

def consultar_db():
    # Creamos una conexión con la base de datos
    con = sqlite3.connect('db_finanzas.db')

    # Creamos el curso para interactuar con los datos
    cursor = con.cursor()

    #x = 15
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

def insertar_db(p_especie,p_precio_apertura,p_transacciones,p_menor_precio,p_mayor_precio,p_fecha_inicio,p_fecha_fin,p_volumen):
    # Creamos una conexión con la base de datos
    con = sqlite3.connect('db_finanzas.db')

    # Creamos el curso para interactuar con los datos
    cursor = con.cursor()
    #print(p_especie,p_precio_apertura,p_transacciones,p_menor_precio,p_mayor_precio,p_fecha_inicio,p_fecha_fin,p_volumen)
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

    # res = cursor.executescript(f'''