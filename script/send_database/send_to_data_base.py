from send_database import db




def insert_to_table(afiliacion, comercio, razon, giro, adquirente, postal_Comercio, postal, 
                            grupo_BBVA, cadena_BBVA,tipo_card, emisor, origen, marca ,codigo_transac ,fecha_op ,
                            moneda ,respuesta_iso ,respuesta_on2 ,codigo_aut ,post_entry_mode ,estatus ,numero_serie_tpv,
                            plataforma , importe ,eci ):
    coneccion=db.conn()
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
        print(id_transaccion)
        print(".................................................")
        
    cur.close()
    coneccion.close()  
    
    
    