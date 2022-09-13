#ref xtra usada: https://es.stackoverflow.com/questions/416227/acceder-a-funciones-desde-otro-archivo-en-python
from funciones import *

print("*****************************************")
print("* SISTEMA DE ALTA Y CONSULTA FINANCIERA *")
print("*****************************************")
print("MENU")
print("1- Actualización de datos")
print("2- Visualización de datos")
print("3. Salir")
opcion_menu_principal=input("Elija opción y presione enter")

if opcion_menu_principal=="1":
    fechas = ingresar_fechas()
    especie = input("Ingrese la especie financiera a consultar")
    consultar_api_finanzas(especie, fechas[0], fechas[1])
elif opcion_menu_principal=="2":
    print("Visulaización de datos")
    consultar_db()
elif opcion_menu_principal=="3":
    print("Salir")
else:
    print("Opción incorrecta")





#insertar_db("arpa_net",21.37,100,20.82,22.03,"2020-02-29","2021-12-04",253000)
#insertar_db("arpa_net2",21.343,100,20.82,22.03,"2020-02-29","2021-12-04",253000)

