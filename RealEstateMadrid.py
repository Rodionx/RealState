from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from modeloRent_Price_prediction import prediccion_precio,distritos,house_types,floors

app = FastAPI()

# Create the templates object for rendering Jinja2 templates
templates = Jinja2Templates(directory="templates")


# Route to render the form with dynamic options
@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "valid_distritos": distritos,
        "valid_house_types": house_types,
        "valid_floors":floors
    })

# Route to handle the form submission and predict the price
@app.post("/predict")
async def predict(
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
    # Call the prediction function
    predicted_price = prediccion_precio(
        sq_mt_built, buy_price, n_rooms, n_bathrooms, has_parking,
        is_new_development, is_renewal_needed, distrito, house_type, floor
    )

    # Return the predicted price and form inputs
    return {
        "Predicted Price": predicted_price,
        "Inputs": {
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
    }