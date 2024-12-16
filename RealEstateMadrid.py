from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from modeloRent_Price_prediction import prediccion_precio,distritos,house_types,floors
from Insert import insert_prediction

app = FastAPI()

templates = Jinja2Templates(directory="templates") #busca index.html en el directorio templates


@app.get("/", response_class=HTMLResponse) 
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", { # Validacion de datos para un dropdown menu en el HTML con las listas creadas en el modelo 
        "request": request,
        "valid_distritos": distritos,
        "valid_house_types": house_types,
        "valid_floors":floors
    })


@app.post("/predict") # Llama a la funcion de predcción
async def predict(request: Request, #Extrae los datos del los formularios con los id correspondientes en el html
    # ID's ↓
    sq_mt_built: float = Form(...),
    buy_price: float = Form(...),
    n_rooms: int = Form(...),
    n_bathrooms: int = Form(...),
    has_parking: int = Form(...),
    is_new_development: int = Form(...),
    is_renewal_needed: int = Form(...),
    distrito: str = Form(...),
    house_type: str = Form(...),
    floor: str = Form(...)
):
    predicted_price = prediccion_precio( #llama a la funcion prediccion precio
        sq_mt_built, buy_price, n_rooms, n_bathrooms, has_parking,
        is_new_development, is_renewal_needed, distrito, house_type, floor
    )
    global results
    results =   {
            "rent_price": predicted_price,
            "sq_mt_built": sq_mt_built,
            "buy_price": buy_price,
            "n_rooms": n_rooms,
            "n_bathrooms": n_bathrooms,
            "has_parking": has_parking,
            "is_new_development": is_new_development,
            "is_renewal_needed": is_renewal_needed,
            "distrito": distrito,
            "house_type": house_type,
            "floor": floor
            }
    return templates.TemplateResponse("PredictPage.html", {"request": request, "results": results})



# Ruta para insertar datos usando FastAPI
@app.post("/insert")
async def insert_data():
    insert_prediction(data=results)
    return {"message": "Sus datos han sido insertados con exito"}
