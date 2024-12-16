import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler

df_Madrid_RealEstate = pd.read_csv('Output/Madrid_Real_Estate_Def')

# Extraccion de Distritos y zonas y tipos de casas para la API

distritos = set(df_Madrid_RealEstate['neighborhood_id'])
distritos = list(distritos)

house_types = set(df_Madrid_RealEstate['house_type_id'])
house_types = list(house_types)


floors = set(df_Madrid_RealEstate['floor'])
floors = list(floors)

#Codificacion de variables no numericas


## Variables Binarias - TRUE OR FALSE - COLUMNAS: has_parking,is_new_development,is_renewal_needed

df_Madrid_RealEstate['has_parking'] = df_Madrid_RealEstate['has_parking'].apply(lambda x:1 if x == True else 0)
df_Madrid_RealEstate['is_new_development'] = df_Madrid_RealEstate['is_new_development'].apply(lambda x:1 if x == True else 0)
df_Madrid_RealEstate['is_renewal_needed'] = df_Madrid_RealEstate['is_renewal_needed'].apply(lambda x:1 if x == True else 0)

##Variables Categoricas - > DUMMIES - COLUMNAS: neighborhood_id,floor,house_type_id

df_Madrid_RealEstate = pd.get_dummies(df_Madrid_RealEstate, columns = ['house_type_id'], drop_first=False,dtype=int)
df_Madrid_RealEstate = pd.get_dummies(df_Madrid_RealEstate, columns = ['neighborhood_id'], drop_first=False,dtype=int)
df_Madrid_RealEstate = pd.get_dummies(df_Madrid_RealEstate, columns = ['floor'], drop_first=False,dtype=int)



df_Madrid_RealEstate_para_modelo = df_Madrid_RealEstate.drop(columns=[('title')])
print(df_Madrid_RealEstate_para_modelo.columns) # Data columns (total 47 columns):

# Creacion de Datasets Para el Modelo
df_train, df_test = train_test_split(df_Madrid_RealEstate_para_modelo, 
                                     test_size=0.2,
                                     random_state=42,
                                     shuffle=True)
#Datasets de Entrenamiento
x_train = df_train.drop('rent_price',axis=1)
y_train=df_train['rent_price'].copy()

#Datasets de Testeo
x_test = df_test.drop('rent_price',axis=1)
y_test=df_test['rent_price'].copy()

# Creacion de la regresion lineal y predicciones
regresion = LinearRegression()
regresion.fit(x_train,y_train)

#Predicciones y bondad del modelo con df de entrenamiento
y_predicciones = regresion.predict(x_train)
error_cuad_medio = mean_squared_error(y_train,y_predicciones)
error_medio=np.sqrt(error_cuad_medio)
error_absol_medio=mean_absolute_error(y_train,y_predicciones)
r_cuadrado = r2_score(y_train,y_predicciones)

print('TRAINING')
print(f"Error Cuadrático Medio: {error_cuad_medio:.4f}")
print(f"Error Medio (RMSE): {error_medio:.4f}")
print(f"Error Absoluto Medio: {error_absol_medio:.4f}")
print(f"R^2 : {r_cuadrado:.4f}")

#Predicciones y bondad del modelo con variables de test

y_predicciones_test = regresion.predict(x_test)
error_cuad_medio = mean_squared_error(y_test,y_predicciones_test)
error_medio=np.sqrt(error_cuad_medio)
error_absol_medio=mean_absolute_error(y_test,y_predicciones_test)
r_cuadrado = r2_score(y_test,y_predicciones_test)

print('TEST')
print(f"Error Cuadrático Medio: {error_cuad_medio:.4f}")
print(f"Error Medio (RMSE): {error_medio:.4f}")
print(f"Error Absoluto Medio: {error_absol_medio:.4f}")
print(f"R^2 : {r_cuadrado:.4f}")

### NOTA: La Variable buy_price añade casi 0.7 de bondad al modelo.

def prediccion_precio(sq_mt_built, buy_price, n_rooms, n_bathrooms, has_parking,
                      is_new_development, is_renewal_needed, distrito, house_type, floor):

    input_user = {
        'sq_mt_built': sq_mt_built,
        'buy_price': buy_price,
        'n_rooms': n_rooms,
        'n_bathrooms': n_bathrooms,
        'has_parking': has_parking,
        'is_new_development': is_new_development,
        'is_renewal_needed': is_renewal_needed
    }

    district_dummies = pd.get_dummies(pd.Series([distrito]), prefix='neighborhood_id')
    house_type_dummies = pd.get_dummies(pd.Series([house_type]), prefix='house_type_id')
    floor_dummies = pd.get_dummies(pd.Series([floor]), prefix='floor')

   
    district_dummies.reset_index(drop=True, inplace=True)
    house_type_dummies.reset_index(drop=True, inplace=True)
    floor_dummies.reset_index(drop=True, inplace=True)

    df_a_predecir = pd.DataFrame([input_user])
    df_a_predecir = pd.concat([df_a_predecir, district_dummies, house_type_dummies, floor_dummies], axis=1)
    
    # Verificar Por Columnas Faltantes entre nuestro dataset y el de entrenamiento
    for col in x_test.columns:
        if col not in df_a_predecir.columns:
            df_a_predecir[col] = 0

    # Re organizarlas acorde x_test        
    df_a_predecir = df_a_predecir.reindex(columns=x_test.columns, fill_value=0)


    predicciones = regresion.predict(df_a_predecir)[0]
    return predicciones

#Test de Prediccion_precio
''' 
input_data = prediccion_precio(75, 320000, 3, 2, 1, True, False, 'District 11: Moncloa', 'HouseType 4: Dúplex','2')
print(input_data)
'''

