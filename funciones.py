from datetime import datetime

def ingresar_fechas():
    # referencia extra usada:   https://parzibyte.me/blog/2020/04/23/validar-fecha-python/
    b_fecha_inicio = 0  # bandeara oara conocer el estado de la fecha inicio ingresada
    b_fecha_fin = 0  # bandeara oara conocer el estado de la fecha fin ingresada
    while b_fecha_inicio == 0:
        try:
            fecha_inicio = input("Ingresa la feha inicio de su consulta en el formato YYYY/MM/DD: ")
            fecha = datetime.strptime(fecha_inicio, '%Y/%m/%d')
            # print("Fecha válida")
            b_fecha_inicio = 1
        except ValueError:
            print("Fecha inicial inválida, por favor reingrésela")
            b_fecha_inicio = 0  # si la fecha ingrfesada no es valida, repite el ciclo hasta que este correcta.

    while b_fecha_fin == 0:
        try:
            fecha_fin = input("Ingresa la feha final de su consulta en el formato YYYY/MM/DD: ")
            fecha = datetime.strptime(fecha_fin, '%Y/%m/%d')
            # print("Fecha final válida")
            b_fecha_fin = 1

        except ValueError:
            print("Fecha final inválida, por favor reingrésela")
            b_fecha_fin = 0  # si la fecha ingrfesada no es valida, repite el ciclo hasta que este correcta.

    if fecha_fin < fecha_inicio:  # verificamos si la fecha final es mayor que la inicial, si no es así las invertimos
        print(
            "Nota: al ser la fecha inicial posterior a la fecha final, se invertirán las mismas para proporcionar el rango correcto de fechas en su consulta")
        fecha_auxiliar = fecha_fin
        fecha_fin = fecha_inicio
        fecha_inicio = fecha_auxiliar

    #print("fecha inicial: ", fecha_inicio)
    #print("fecha final: ", fecha_fin)
    return([fecha_inicio,fecha_fin])
