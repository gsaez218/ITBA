#ref xtra usada: https://es.stackoverflow.com/questions/416227/acceder-a-funciones-desde-otro-archivo-en-python
from funciones import *
import requests
import json


# Obtenemos la información del mensaje en formato JSON del repositorio consultando la API
json_file = requests.get("https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2022-08-18/2022-08-21?adjusted=true&sort=asc&limit=120&apiKey=kgNXTHqp5bQH1_H3RcUbUQFk73CB59Z3")
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
 # print(lista_resultados)
  #print(type(lista_resultados))
  #aqui recorremos los difernetes valores de la lista y los mostramos (aca iran guardandose los registros en la BD)
  for indice in lista_resultados:
    print("Volúmen = ",indice['v'])
    print("Precio de apertura = ",indice['o'])
    print("Transacciones = ",indice['n'])
    print("Menor precio = ",indice['l'])
    print("Mayor precio = ",indice['h'])

fechas=ingresar_fechas()
print("respuestas de la funcion: ",fechas)