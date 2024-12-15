#Fichero Exclusivamente Documental, para la revisar el historia de cambios del dataset

import pandas  as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re

houses_df = pd.read_csv("Dataset\\houses_Madrid.csv")
#print(houses_df.info())

houses_df = houses_df.drop(columns = ['Unnamed: 0']) 
#houses_df = houses_df.dropna(axis='columns')

#print(houses_df.columns)

#print(houses_df.info())

#print(houses_df.head())

house_df_def = houses_df[      [ 
                                'title',
                                'sq_mt_built',
                                'neighborhood_id',
                                'buy_price',
                                'rent_price',
                                'n_rooms',
                                'n_bathrooms',
                                'has_parking',
                                'is_new_development',
                                'floor',
                                'is_renewal_needed',
                                'house_type_id']
                                ]



### EXPLORACION DE VARIABLES
''''

price = house_df_def['rent_price']
sq_mt_built = house_df_def['sq_mt_built']
buy_price = house_df_def['buy_price']
n_rooms = house_df_def['n_rooms']
neighborhood =  house_df_def['neighborhood_id']

price = pd.Series([abs(x) if x < 0 else x for x in price])  #convierte negaitvos a positivos

def min_max(serie): #Normalización Min Max
    minValor = serie.min()
    maxValor = serie.max()
    serie_minmax = (serie - minValor) / (maxValor - minValor)
    return serie_minmax

price = min_max(price)

print(price.describe())

plt.hist(price,density=False,bins=10,alpha=0.6,color='b')
plt.show

'''
#floor = set(house_df_def['floor'])
#floor = list(floor)
#print(floor)
#NOTA: Hay mucha desviación entre los precios con minimos de 18 y maximos de 61k
## Lo mejor por ahora seria deshacerse de esos outliers y probar con los datos que tenemos



house_df_def = house_df_def.dropna()



print(house_df_def.info())
house_df_def['rent_price'] = ([abs(x) if x < 0 else x for x in house_df_def['rent_price']])

'''
house_df_def.describe().apply(lambda x: x.apply('{0:.5f}'.format))#Describe sin notacion cientifica



plt.scatter(house_df_def['rent_price'],house_df_def['rent_price'].index)
plt.show

plt.scatter(house_df_def['buy_price'],house_df_def['buy_price'].index)
plt.show 

'''
### Deteccion y filtrado de atipicos
print(house_df_def.columns)

houses_df_filtrado = house_df_def[(np.abs(stats.zscore(house_df_def[['buy_price','rent_price']])) <  1).all(axis=1)]
# ^ Filtra datos a 1 desviación estandar de la media


'''
plt.scatter(df_precios['rent_price'],df_precios['rent_price'].index)
plt.show
'''
'''
plt.scatter(df_precios['buy_price'],df_precios['buy_price'].index)
plt.show
'''

print(houses_df_filtrado.columns)

print(houses_df_filtrado.info())

print(houses_df_filtrado.describe().apply(lambda x: x.apply('{0:.5f}'.format)))#Describe sin notacion cientifica

houses_df_filtrado['neighborhood_id'] =  houses_df_filtrado['neighborhood_id'].apply(lambda x: re.search(r'(District \d+: [\w\s]+)', x).group(0))
#Elimina los barrios y deja la string solo en distritos 

houses_df_filtrado.to_csv("Output//Madrid_Real_Estate_Def")