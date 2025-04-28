# Proyecto de Migración de Datos: PostgreSQL a MongoDB

## Descripción

Este proyecto permite migrar automáticamente los datos de todas las tablas de una base de datos PostgreSQL a una base de datos MongoDB.
La migración mantiene el orden de las tablas según las dependencias de claves foráneas para evitar errores de integridad referencial.

El script se conecta a ambas bases de datos, calcula el orden de migración, transforma los datos (por ejemplo, fechas y decimales) para que sean compatibles con MongoDB, y los inserta como documentos en las respectivas colecciones.

## Tecnologías Utilizadas

- Python 3.8+
- Asyncio
- AsyncPG (Cliente asíncrono para PostgreSQL)
- PyMongo (Cliente para MongoDB)

## Configuración Inicial

1. Instalar las dependencias necesarias:

```bash
pip install asyncpg pymongo
```

2. Configurar las credenciales de conexión:

- **PostgreSQL:** Editar el diccionario `POSTGRES_CONFIG` con tus datos de conexión.
- **MongoDB:** Modificar `MONGO_URI` con tu URI de conexión.

```python
POSTGRES_CONFIG = {
    'user': 'postgres',
    'password': '<tu_contra>',
    'database': 'postgres',
    'host': 'localhost',
    'port': 5432,
}

MONGO_URI = "mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
```

## Ejecución del Script

Simplemente ejecuta el script principal:

```bash
python migracion.py
```

Este script realizará:

1. Conexión a PostgreSQL.
2. Conexión a MongoDB.
3. Cálculo del orden correcto de migración de las tablas.
4. Migración de datos de cada tabla a su colección correspondiente en MongoDB.
5. Cierre seguro de ambas conexiones.

## Lógica del Código

### Conexión
- `conectar_postgres()`: Establece conexión asíncrona con PostgreSQL.
- `conectar_mongodb()`: Establece conexión con MongoDB y verifica con un `ping`.

### Orden de Migración
- `calcular_orden_tablas()`:
  - Identifica tablas independientes (sin claves foráneas).
  - Construye un grafo de dependencias.
  - Aplica una ordenación topológica (tipo BFS) para determinar el orden seguro de migración.

### Migración de Datos
- `migrar_tablas_a_mongo()`:
  - Obtiene las columnas de cada tabla.
  - Extrae todos los datos.
  - Convierte tipos especiales (fecha, decimal) compatibles con MongoDB.
  - Inserta los datos en la colección correspondiente.

### Utilidades de Conversión
- `convertir_a_datetime()`: Transforma objetos `date` en `datetime`.
- `convertir_a_float()`: Transforma objetos `Decimal` en `float`.

## Ejemplo de Salida

```plaintext
✅ Conectado exitosamente a PostgreSQL.
✅ Pinged your deployment. Connected to MongoDB!

🎯 Ambas conexiones exitosas. Inicio de la migración.
['usuarios', 'productos', 'ordenes']
✅ Migrada la tabla 'usuarios' con 150 documentos.
✅ Migrada la tabla 'productos' con 80 documentos.
✅ Migrada la tabla 'ordenes' con 300 documentos.

🔒 Conexión a PostgreSQL cerrada.
🔒 Conexión a MongoDB cerrada.
```

## Consideraciones

- Las tablas sin datos serán ignoradas de forma segura.
- Las fechas y decimales son convertidos automáticamente para compatibilidad.
- Si una tabla tiene errores durante la migración, el error se mostrará en la consola pero no detendrá el proceso general.

## Futuras Mejoras

- Implementar migración incremental o por lotes.
- Manejar datos anidados o relaciones entre documentos.
- Agregar configuración vía archivos `.env` o `config.json`.
- Mejorar la tolerancia a errores y generar reportes de migración.

---

¡Feliz migración! 🚀

