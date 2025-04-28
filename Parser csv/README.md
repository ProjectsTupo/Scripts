# Formateo de Fechas en un Archivo CSV

Este pequeño script en Python utiliza el módulo `csv` para leer un archivo CSV de ventas y formatea la columna de fecha (`fecha_venta`) agregando comillas simples alrededor de cada fecha.

## Archivos Involucrados

- **Entrada**: `ventas_original.csv`  
  Archivo original que contiene los datos de ventas.

- **Salida**: `ventas_formateado.csv`  
  Archivo que será generado con las fechas formateadas.

## Funcionamiento del Script

1. **Lectura del archivo original**:
   - Se abre `ventas_original.csv` en modo lectura.
   - Se utiliza `csv.reader` para procesar el contenido.

2. **Escritura en el nuevo archivo**:
   - Se crea `ventas_formateado.csv` en modo escritura.
   - Se utiliza `csv.writer` para guardar los datos formateados.

3. **Procesamiento**:
   - Se copia el encabezado tal cual.
   - Se identifica el índice de la columna `fecha_venta`.
   - Para cada fila, se agrega comillas simples alrededor del valor de la fecha.
   - Se escribe la fila modificada en el nuevo archivo.

4. **Mensaje de éxito**:
   - Una vez finalizado, se imprime en consola: `✅ Archivo generado: ventas_formateado.csv`

## Requisitos

- Python 3.6 o superior.

(No es necesario instalar librerías adicionales, ya que `csv` es parte de la biblioteca estándar de Python).

## Ejecución

Puedes ejecutar el script simplemente corriéndolo en tu terminal:

```bash
python nombre_del_script.py
```

Recuerda tener el archivo `ventas_original.csv` en el mismo directorio o actualizar el path según corresponda.

## Notas

- Si la columna `fecha_venta` no existe, el script fallará al lanzar una excepción.
- Este script **no modifica** el archivo original.
- El nuevo archivo contendrá las mismas filas pero con la fecha rodeada de comillas simples.

---

✨ Hecho para facilitar el preformateo de datos que requieran formato específico en fechas, especialmente para exportaciones hacia bases de datos o sistemas que requieran fechas entre comillas.

