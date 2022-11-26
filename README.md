# Proyecto Flota 2
Entrada del sistema

El programa recibe por HTTP la información de cada viaje realizado por nuestra flota, el JSON que reciba debe tener al menos la siguiente información:

Año-Mes-día del viaje efectuado
Identificador del vehículo
¿Cuánto tiempo el vehículo tardó en llegar a destino (tiempo circulando)? [Valor en minutos].
¿Cuánto recaudó por ese viaje?

Salida del sistema

Se deberá poder extraer de la base de datos un resumen con los siguientes resultados (y cualquier otro que desee agregar el alumno):

¿Cuántos viajes realizó un determinado vehículo ingresado por consola?
¿Cuánto tiempo estuvo circulando el vehículo?
¿Cuánta recaudación logró el vehículo?
Se deberá especificar el día, mes o año en donde se desea realizar el análisis para el vehículo ingresado. Toda la información necesaria para crear el reporte se debe enviar por HTTP.
