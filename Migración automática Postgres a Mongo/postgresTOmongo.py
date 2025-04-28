import asyncio
import asyncpg
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from collections import defaultdict, deque
from datetime import datetime, date
from decimal import Decimal

POSTGRES_CONFIG = {
    'user': 'postgres',
    'password': '<tu_contra>',
    'database': 'postgres',
    'host': 'localhost',
    'port': 5432,
}

MONGO_URI = "mongodb+srv://lazaro:<tu_contra>@mycluster.nqbaurt.mongodb.net/?retryWrites=true&w=majority&appName=MyCluster"
MONGO_DB = "MongoMigrado"

async def main():
    # Conexión a PostgreSQL
    pg_conn = await conectar_postgres()

    # Conexión a MongoDB
    mongo_client = conectar_mongodb()

    if pg_conn and mongo_client:
        print("\n🎯 Ambas conexiones exitosas. Inicio de la migración.")

        orden_tablas = await calcular_orden_tablas(pg_conn)
        print(orden_tablas)
        await migrar_tablas_a_mongo(pg_conn, mongo_client, orden_tablas)

    # Cierre de conexiones
    if pg_conn:
        await pg_conn.close()
        print("🔒 Conexión a PostgreSQL cerrada.")

    if mongo_client:
        mongo_client.close()
        print("🔒 Conexión a MongoDB cerrada.")

async def calcular_orden_tablas(pg_conn):
    query_indep = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
          AND table_name NOT IN (
            SELECT DISTINCT tc.table_name
            FROM information_schema.table_constraints AS tc
            WHERE tc.constraint_type = 'FOREIGN KEY'
          );
    """
    independientes = {row['table_name'] for row in await pg_conn.fetch(query_indep)}

    query_deps = """
        SELECT DISTINCT tc.table_name AS dependiente, ccu.table_name AS referenciada
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY';
    """
    dependencias = [(row['dependiente'], row['referenciada']) for row in await pg_conn.fetch(query_deps)]

    # Grafo dirigido en formato adjacency list
    grafo = defaultdict(list)
    in_degree = defaultdict(int)

    # Construir el grafo y contar los grados de entrada
    for destino, origen in dependencias:
        grafo[origen].append(destino)
        in_degree[destino] += 1
        if origen not in in_degree:
            in_degree[origen] = 0

    # Topología de los nodos por nivel
    nodos_por_nivel = []
    nodos_sin_dependencia = deque([nodo for nodo, grado in in_degree.items() if grado == 0])

    # Algoritmo de ordenación topológica (BFS)
    while nodos_sin_dependencia:
        nivel = []
        for _ in range(len(nodos_sin_dependencia)):
            nodo = nodos_sin_dependencia.popleft()
            nivel.append(nodo)
            for vecino in grafo[nodo]:
                in_degree[vecino] -= 1
                if in_degree[vecino] == 0:
                    nodos_sin_dependencia.append(vecino)
        if nivel:
            nodos_por_nivel.append(nivel)

    # Concatenar todas las listas en una sola
    resultado_concatenado = [nodo for nivel in nodos_por_nivel for nodo in nivel]
    orden = list(dict.fromkeys(list(independientes) + resultado_concatenado))

    return orden

async def migrar_tablas_a_mongo(pg_conn, mongo_client, orden_tablas):
    db_mongo = mongo_client.get_database(MONGO_DB)

    for tabla in orden_tablas:
        try:
            # 1. Obtener las columnas de la tabla
            query_columnas = f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = '{tabla}';
            """
            columnas = [row['column_name'] for row in await pg_conn.fetch(query_columnas)]

            # 2. Obtener los datos de la tabla
            query_datos = f'SELECT * FROM "{tabla}";'
            filas = await pg_conn.fetch(query_datos)

            documentos = []

            # 3. Formatear los datos como documentos de Mongo
            for fila in filas:
                doc = {}
                for columna in columnas:
                    valor = fila[columna]
                    # Convertir fechas a datetime si es necesario
                    valor = convertir_a_datetime(valor)
                    valor = convertir_a_float(valor)
                    doc[columna] = valor
                documentos.append(doc)

            if documentos:
                # 4. Insertar los documentos en MongoDB
                coleccion = db_mongo.get_collection(tabla)
                coleccion.insert_many(documentos)
                print(f"✅ Migrada la tabla '{tabla}' con {len(documentos)} documentos.")
            else:
                print(f"⚠️ La tabla '{tabla}' no tiene datos para migrar.")

        except Exception as e:
            print(f"❌ Error migrando la tabla '{tabla}': {e}")

# Función para convertir datetime.date a datetime.datetime
def convertir_a_datetime(fecha):
    if isinstance(fecha, datetime):  # Verifica si es un objeto datetime
        return fecha
    elif isinstance(fecha, date):  # Verifica si es un objeto datetime.date
        # Convertir a datetime, asignando la hora a las 00:00:00
        return datetime.combine(fecha, datetime.min.time())
    return fecha  # Si no es una fecha, se deja tal cual

# Función para convertir Decimal a float
def convertir_a_float(valor):
    if isinstance(valor, Decimal):
        return float(valor)  # Convertir Decimal a float
    return valor  # Si no es Decimal, se deja tal cual

async def conectar_postgres():
    try:
        conn = await asyncpg.connect(**POSTGRES_CONFIG)
        print("✅ Conectado exitosamente a PostgreSQL.")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def conectar_mongodb():
    try:
        client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("✅ Pinged your deployment. Connected to MongoDB!")
        return client
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(main())
