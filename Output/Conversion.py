import sqlite3
import csv

def csv_to_sqlite(csv_file, sqlite_db, table_name):
    # Conectar o crear la base de datos SQLite
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    # Leer el archivo CSV y extraer los encabezados
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Leer la primera fila como encabezados

        # Crear la tabla en SQLite
        columns = ', '.join([f'"{header}" TEXT' for header in headers])
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')

        # Insertar los datos
        for row in reader:
            placeholders = ', '.join(['?'] * len(row))
            cursor.execute(f'INSERT INTO {table_name} VALUES ({placeholders})', row)

    # Confirmar y cerrar la conexión
    conn.commit()
    conn.close()

    print(f'El archivo CSV se ha convertido exitosamente a {sqlite_db} en la tabla {table_name}.')


csv_file = '/Users/rodion/Desktop/RealState/Output/Madrid_Real_Estate_Def'  # Reemplaza con la ruta a tu archivo CSV
sqlite_db = 'Madrid_Real_Estate_Def.db'  # Ruta a tu base de datos SQLite
table_name = 'Datos'  # Nombre de la tabla en SQLite

csv_to_sqlite(csv_file, sqlite_db, table_name)
