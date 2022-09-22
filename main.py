#ref xtra usada: https://es.stackoverflow.com/questions/416227/acceder-a-funciones-desde-otro-archivo-en-python
from funciones import *




import pandas as pd
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


consultar_pandas_db()

#fig = plt.figure()  # an empty figure with no Axes
#fig, ax = plt.subplots()  # a figure with a single Axes
fig, axs = plt.subplots(3, 3)  # a figure with a 2x2 grid of Axes

mpl.use('TkAgg')

ts = pd.Series(random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot()
plt.show()
print(mpl.get_backend())

x = np.linspace(0, 2, 100)  # Sample data.

# Note that even in the OO-style, we use `.pyplot.figure` to create the Figure.
fig, ax = plt.subplots(figsize=(5, 2.7))
ax.plot(x, x, label='linear')  # Plot some data on the axes.
ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
ax.plot(x, x**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend();  # Add a legend.
plt.show()
####################################################################







#%matplotlib inline



















"""
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
        os.system("cls")
        print("Gracias por usar nuestros servicios")
        break
    else:
        print("Opción incorrecta")
"""





#insertar_db("arpa_net",21.37,100,20.82,22.03,"2020-02-29","2021-12-04",253000)
#insertar_db("arpa_net2",21.343,100,20.82,22.03,"2020-02-29","2021-12-04",253000)

