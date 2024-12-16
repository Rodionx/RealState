import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ruta al archivo de la base de datos y los datos de la imagen
db_path = 'Madrid_Real_Estate_Def.db'

# Datos extraídos de la imagen
default_data = {
    "square_meters_built": 100,
    "buying_price": 200000,
    "number_of_rooms": 3,
    "number_of_bathrooms": 2,
    "has_parking": 'Yes',
    "is_new_development": 'No',
    "is_renewal_needed": 'Yes',
    "distrito": 'Centro',
    "house_type": 'Apartment',
    "floor": 5,
    "predicted_price": 250000
}

# Modelo para recibir datos desde el cliente
class PredictionData(BaseModel):
    square_meters_built: int
    buying_price: int
    number_of_rooms: int
    number_of_bathrooms: int
    has_parking: str
    is_new_development: str
    is_renewal_needed: str
    distrito: str
    house_type: str
    floor: int
    predicted_price: int

# Función para insertar datos en la base de datos SQLite
def insert_prediction(db_path, data):
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
      
        
        # Insertar los datos
        cursor.execute('''
            INSERT INTO predicciones (
                square_meters_built, buying_price, number_of_rooms, number_of_bathrooms, 
                has_parking, is_new_development, is_renewal_needed, distrito, house_type, 
                floor, predicted_price
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''', (
            data.square_meters_built,
            data.buying_price,
            data.number_of_rooms,
            data.number_of_bathrooms,
            data.has_parking,
            data.is_new_development,
            data.is_renewal_needed,
            data.distrito,
            data.house_type,
            data.floor,
            data.predicted_price
        ))
        
        # Guardar cambios y cerrar conexión
        conn.commit()
        return {"status": "success", "message": "Datos insertados correctamente."}
    except sqlite3.Error as e:
        return {"status": "error", "message": f"Error al insertar los datos: {e}"}
    finally:
        conn.close()

# Ruta principal que renderiza el formulario HTML
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Ruta para insertar datos usando FastAPI
@app.post("/insert")
def insert_data(data: PredictionData):
    result = insert_prediction(db_path, data)
    return JSONResponse(content=result)