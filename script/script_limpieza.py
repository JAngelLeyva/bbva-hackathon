
import boto3
import os
import io
import pandas as pd
import unidecode


from cleaning import cleaning_data
from send_database import send_to_data_base

"""
linux
export AWS_ACCESS_KEY_ID=AKIAWX5GLZKAQHO77HOL
export AWS_SECRET_ACCESS_KEY=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
export AWS_DEFAULT_REGION=us-east-2
"""

resource = boto3.client(
    service_name='s3',
    aws_access_key_id = 'AKIAWX5GLZKAQHO77HOL',
    aws_secret_access_key = '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',
    region_name = 'us-east-2'
)

def main(bucketName,fileName):
    objetc=resource.get_object(Bucket=bucketName,Key=fileName)
    #for obj in resource.Bucket(bucketName).objects.all():
    
    df=pd.DataFrame([])
    
    if objetc['ContentType']== 'text/csv':
        
        print("Archivo tipo csv")
        data = objetc['Body'].read()
        s=str(data,'latin-1')
        unaccented_string = unidecode.unidecode(s)
        datas = io.StringIO(unaccented_string) 
        df=pd.read_csv(datas, sep=",")

    
    else:
        print("Formato del archivo no valido")
    
    df=cleaning_data.limpieza(df)
    
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
        
        send_to_data_base.insert_to_table(afiliacion, comercio, razon, giro, adquirente, postal_Comercio, postal, 
                            grupo_BBVA, cadena_BBVA,tipo_card, emisor, origen, marca ,codigo_transac ,fecha_op ,
                            moneda ,respuesta_iso ,respuesta_on2 ,codigo_aut ,post_entry_mode ,estatus ,numero_serie_tpv,
                            plataforma , importe ,eci )

    print("Terminado")

if __name__ == "__main__":
    #app.run_server(host="0.0.0.0", port="8050", debug=True)
    main('hackathon-test-bbva-2021','Log Transacional layout tunel.csv')
       # print(obj)
    #resource.Bucket(bucket)