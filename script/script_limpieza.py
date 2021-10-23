import json
import numpy as np
import pandas as pd 
import boto3 
import psycopg2, psycopg2.extras
import unidecode
import os
import io
import urllib.parse

DB = os.environ.get('DB')
USER = os.environ.get('USER')
PORT = os.environ.get('PORT')
PASSWORD = os.environ.get('PASSWORD')
HOST=os.environ.get('HOST')

def conn():
    conn = psycopg2.connect(database=DB,user=USER,password=PASSWORD,host=HOST, port=PORT)
    return conn

def insert_to_table(afiliacion, comercio, razon, giro, adquirente, postal_Comercio, postal, 
                            grupo_BBVA, cadena_BBVA,tipo_card, emisor, origen, marca ,codigo_transac ,fecha_op ,
                            moneda ,respuesta_iso ,respuesta_on2 ,codigo_aut ,post_entry_mode ,estatus ,numero_serie_tpv,
                            plataforma , importe ,eci ):
    coneccion=conn()
    cur = coneccion.cursor()
    try:
        SQL="INSERT INTO public.transacional (afiliacion, comercio, razon, giro, adquirente, postal_Comercio, postal, \
                            grupo_BBVA, cadena_BBVA,tipo_card, emisor, origen, marca ,codigo_transac ,fecha_op ,\
                            moneda ,respuesta_iso ,respuesta_on2 ,codigo_aut ,post_entry_mode ,estatus ,numero_serie_tpv,\
                            plataforma , importe ,eci )\
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data=(str(afiliacion), str(comercio), str(razon), str(giro), str(adquirente), str(postal_Comercio), str(postal), 
                            str(grupo_BBVA), str(cadena_BBVA),str(tipo_card), str(emisor), str(origen), str(marca),
                            str(codigo_transac),str(fecha_op),str(moneda) ,str(respuesta_iso) ,str(respuesta_on2) ,
                            str(codigo_aut) ,str(post_entry_mode) ,str(estatus) ,str(numero_serie_tpv),
                            str(plataforma) , str(importe) ,str(eci))
        
        cur.execute(SQL, data)      
        coneccion.commit()
    except psycopg2.Error as e:
        print("Unable to connect!")
        print(e.pgerror)
        print(e.diag.message_detail)
        print("submit failed")
        print(respuesta_iso)
        print(".................................................")
        
    cur.close()
    coneccion.close() 

def limpieza(df):
    try:
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
    except:
        print("Errores en drop-columns")
    try:
        df['Fecha de operacion']=pd.to_datetime(df['Fecha de operacion'])
    except:
        print("Errores en datetime")
    
    df['Numero de serie TPV']=df['Numero de serie TPV'].apply(lambda x:'NOT' if x =='' else x)
    try:
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
        
    except:
        print('lower failed D:')
    df['Codigo de respuesta ISO']=df['Codigo de respuesta ISO'].astype(str)
    df['nuevo']=df['Codigo de respuesta ISO'].str.split("-")
    df.columns= df.columns.str.strip().str.lower()
    
    return df


def lambda_handler(event, context):
    # TODO implement    
    
    resource = boto3.client(
    service_name='s3',
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID1'),
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY1'),
    region_name = os.environ.get('AWS_DEFAULT_REGION1')
    )
    bucket=event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    objetc=resource.get_object(Bucket=bucket, Key=key)
    data = objetc['Body'].read()
    s=str(data,'latin-1')
    unaccented_string = unidecode.unidecode(s)
    datas = io.StringIO(unaccented_string)
    df=pd.read_csv(datas, sep=",")
    #print(objetc['ContentType'])
    df=limpieza(df)
    for row in range(df.shape[0]):
        afiliacion=df['afiliacion'].loc[row]
        comercio=df['nombre del comercio'].loc[row]
        razon=df['razon social'].loc[row]
        giro=df['giro del comercio'].loc[row]
        adquirente=df['adquirente'].loc[row]
        postal_Comercio=df['codigo postal (comercios)'].loc[row]
        postal=df['codigo postal'].loc[row]
        grupo_BBVA=df['grupo bbva'].loc[row]
        cadena_BBVA=df['cadena bbva'].loc[row]
        tipo_card=df['tipo de tarjeta'].loc[row]
        emisor=df['emisor'].loc[row]
        origen=df['origen'].loc[row]
        marca=df['marca'].loc[row]
        codigo_transac=df['codigo de transaccion'].loc[row]
        fecha_op=df['fecha de operacion'].loc[row]
        moneda=df['moneda'].loc[row]
        respuesta_iso=df['codigo de respuesta iso'].loc[row]
        respuesta_on2=df['codigo de respuesta on2'].loc[row]
        codigo_aut=df['codigo de autorizacion'].loc[row]
        post_entry_mode=df['pos entry mode'].loc[row]
        estatus=df['estatus'].loc[row]
        numero_serie_tpv=df['numero de serie tpv'].loc[row]
        plataforma=df['plataforma'].loc[row]
        importe=df['importe'].loc[row]
        eci=df['eci'].loc[row]                           
        
        tipo_val=df['nuevo'][row][0]
      
        valor_int=int(tipo_val)
        
        #0-Aprobada  51-Fondos Insuficientes   53-Tarjeta Vencida  54-Tarjeta Vencida 55-PIN invalido / Excedido
        if (valor_int!=0 and valor_int!=51 and valor_int!=53 and valor_int!=54 and valor_int!=55 and codigo_aut!=''):
            insert_to_table(afiliacion, comercio, razon, giro, adquirente, 
                postal_Comercio, postal,grupo_BBVA, cadena_BBVA,tipo_card, 
                emisor, origen, marca ,codigo_transac ,fecha_op , moneda ,
                respuesta_iso ,respuesta_on2 ,codigo_aut ,post_entry_mode ,
                estatus ,numero_serie_tpv, plataforma , importe ,eci )
    print("Finish upload")
    
    return "Sucessczxzczczxcz"