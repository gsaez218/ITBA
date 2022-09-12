#ref xtra usada: https://es.stackoverflow.com/questions/416227/acceder-a-funciones-desde-otro-archivo-en-python

from funciones import *

fechas=ingresar_fechas()
especie=input("Ingrese la especie financiera a consultar")
consultar_api_finanzas(especie,fechas[0],fechas[1])

#insertar_db("AAL",21.34,100,20.82,22.03,"2020-02-29","2021-12-04",253000.23)
#insertar_db("AAL",21.343,100,20.82,22.03,"2020-02-29","2021-12-04",253000.23)
#consultar_db()
