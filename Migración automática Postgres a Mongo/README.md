📦 Migrador de Datos de PostgreSQL a MongoDB
Este proyecto es un script de migración que permite transferir datos de una base de datos PostgreSQL a una base de datos MongoDB, respetando el orden de dependencia entre tablas (gracias a un algoritmo de ordenación topológica).

🚀 ¿Cómo funciona?
El script realiza los siguientes pasos:

Conexión a PostgreSQL (base de datos relacional) y a MongoDB (base de datos NoSQL).

Detección de tablas y sus dependencias:

Identifica tablas independientes (sin llaves foráneas).

Calcula el orden de migración para respetar las relaciones padre-hijo.

Migración de datos:

Extrae todos los registros de cada tabla.

Convierte correctamente los tipos de datos (por ejemplo, fechas o decimales).

Inserta los datos como documentos en colecciones de MongoDB.

Cierre seguro de ambas conexiones.

🛠️ Requisitos
Python 3.8 o superior

Bases de datos ya configuradas:

PostgreSQL funcionando localmente.

MongoDB Atlas (o instancia accesible vía red).

Paquetes de Python:

bash
Copiar
Editar
pip install asyncpg pymongo
📋 Configuración
Antes de ejecutar el script:

Actualiza los siguientes valores en el código:

python
Copiar
Editar
POSTGRES_CONFIG = {
    'user': 'postgres',
    'password': '<tu_contra>',
    'database': 'postgres',
    'host': 'localhost',
    'port': 5432,
}
python
Copiar
Editar
MONGO_URI = "mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
MONGO_DB = "MongoMigrado"
🔥 Importante: No subas tus contraseñas reales a GitHub.

🧠 Estructura del código

Función	Descripción
main()	Orquesta todo el proceso de conexión, migración y cierre.
calcular_orden_tablas(pg_conn)	Calcula el orden correcto en que deben migrarse las tablas.
migrar_tablas_a_mongo(pg_conn, mongo_client, orden_tablas)	Migra los datos tabla por tabla a MongoDB.
convertir_a_datetime(valor)	Convierte fechas de tipo date a datetime.
convertir_a_float(valor)	Convierte valores Decimal a float.
conectar_postgres()	Establece conexión con PostgreSQL de forma asíncrona.
conectar_mongodb()	Establece conexión con MongoDB.
⚙️ ¿Cómo ejecutar?
Abre tu terminal en el directorio del proyecto.

Ejecuta:

bash
Copiar
Editar
python nombre_del_archivo.py
Reemplaza nombre_del_archivo.py por el nombre real del archivo .py que contiene el script.

📚 Conceptos importantes usados
asyncio: Para manejar múltiples tareas de forma asíncrona y eficiente.

asyncpg: Librería para conexión y consultas asíncronas a PostgreSQL.

pymongo: Cliente oficial para interactuar con MongoDB desde Python.

Ordenación topológica: Algoritmo para determinar el orden de migración respetando relaciones padre-hijo entre tablas.

