#ref xtra usada: https://es.stackoverflow.com/questions/416227/acceder-a-funciones-desde-otro-archivo-en-python

from funciones import *


consultar_api_finanzas()

fechas=ingresar_fechas()
print("respuestas de la funcion: ",fechas)