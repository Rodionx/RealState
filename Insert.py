import sqlite3

# Ruta al archivo de la base de datos y los datos de la imagen
db_path = 'Madrid_Real_Estate_Def.db'


# Función para calcular autoincremento

table = "Predicciones"  
get_next_id = lambda db_path, table: (lambda cur: cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] + 1)(
    sqlite3.connect(db_path).cursor()
)

# Obtener el próximo ID
next_id = get_next_id(db_path, table)



# Datos extraídos de la imagen
#         data = {
#             "idPrediccion" : next_id,
#             "rent_price": predicted_price,
#             "sq_mt_built": sq_mt_built,
#             "buy_price": buy_price,
#             "n_rooms": n_rooms,
#             "n_bathrooms": n_bathrooms,
#             "has_parking": has_parking,
#             "is_new_development": is_new_development,
#             "is_renewal_needed": is_renewal_needed,
#             "distrito": distrito,
#             "house_type": house_type,
#             "floor": floor
# }

# Modelo para recibir datos desde el cliente


# Función para insertar datos en la base de datos SQLite
def insert_prediction(data):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print(data)
        
        # Insertar los datos
        cursor.execute('''
            INSERT INTO predicciones (
                idPrediccion, metrosCuadrados, PrecioCompra, numHabitaciones, numBanos, 
                parking, cNueva, reformable, distrito, tipoCasa, 
                planta, prediccion
            ) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (
            next_id,
            data['sq_mt_built'],
            data['buy_price'],
            data['n_rooms'],
            data['n_bathrooms'],
            data['has_parking'],
            data['is_new_development'],
            data['is_renewal_needed'],
            data['distrito'],
            data['house_type'],
            data['floor'],
            data['rent_price']
        ))
        
        # Guardar cambios y cerrar conexión
        conn.commit()
        return {"status": "success", "message": "Datos insertados correctamente."}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Error al insertar los datos: {e}"}
    finally:
        conn.close()

