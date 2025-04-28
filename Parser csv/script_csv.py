import csv

# Nombres del archivo de entrada y salida
archivo_entrada = 'ventas_original.csv'
archivo_salida = 'ventas_formateado.csv'

# Abrimos el archivo original para lectura y uno nuevo para escritura
with open(archivo_entrada, mode='r', newline='', encoding='utf-8') as entrada, \
     open(archivo_salida, mode='w', newline='', encoding='utf-8') as salida:

    lector = csv.reader(entrada)
    escritor = csv.writer(salida)

    # Leer la cabecera
    encabezado = next(lector)
    escritor.writerow(encabezado)

    # Encontrar el índice de la columna fecha_venta
    idx_fecha = encabezado.index('fecha_venta')

    # Recorremos cada fila y agregamos comillas simples a la fecha
    for fila in lector:
        fila[idx_fecha] = f"'{fila[idx_fecha]}'"
        escritor.writerow(fila)

print(f"✅ Archivo generado: {archivo_salida}")