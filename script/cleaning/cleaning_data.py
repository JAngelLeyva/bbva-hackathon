import numpy as np
import pandas as pd


def limpieza(df):
    df=df.drop(columns=['BIN y 4 ultimos digitos', 
                     'Identificador de promocion',
                     'Tipo de plan o promocion',
                     'Plazo',
                     'Skip Payment',
                     'Puntos',
                     'Monto en puntos',
                     'Importe revolvente',
                     'Equivalencia (pesos por punto)',
                    ])
    
    df['Fecha de operacion']=pd.to_datetime(df['Fecha de operacion'])
    
    df['Numero de serie TPV']=df['Numero de serie TPV'].apply(lambda x:'NOT' if x =='' else x)
    
    df['Nombre del comercio']=df['Nombre del comercio'].str.lower()
    df['Razon social']=df['Razon social'].str.lower()
    df['Giro del comercio']=df['Giro del comercio'].str.lower()
    df['Adquirente']=df['Adquirente'].str.lower()
    df['Tipo de tarjeta']=df['Tipo de tarjeta'].str.lower()
    df['Emisor']=df['Emisor'].str.lower()
    df['Origen']=df['Origen'].str.lower()
    df['Marca']=df['Marca'].str.lower()
    df['Codigo de transaccion']=df['Codigo de transaccion'].str.lower()
    df['Moneda']=df['Moneda'].str.lower()
    df['Codigo de respuesta ISO']=df['Codigo de respuesta ISO'].str.lower()
    df['Codigo de respuesta ON2']=df['Codigo de respuesta ON2'].str.lower()
    df['POS Entry Mode']=df['POS Entry Mode'].str.lower()
    df['Estatus']=df['Estatus'].str.lower()
    df['Numero de serie TPV']=df['Numero de serie TPV'].str.lower()
    df['Plataforma']=df['Plataforma'].str.lower()
    df.columns= df.columns.str.strip().str.lower()
    
    return df
    