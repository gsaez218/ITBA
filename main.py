#ref xtra usada: https://es.stackoverflow.com/questions/416227/acceder-a-funciones-desde-otro-archivo-en-python

from funciones import *

fechas=ingresar_fechas()
especie=input("Ingrese la especie financiera a consultar")
consultar_api_finanzas(especie,fechas[0],fechas[1])

