import psycopg2, psycopg2.extras

#Credentials for the database
DB = 'postgres'
USER = 'postgres'
PORT =5432
PASSWORD = 'revolutions'
HOST='database-1.crq3jisl0sbb.us-east-1.rds.amazonaws.com'

def conn():
    conn = psycopg2.connect(database=DB,user=USER,password=PASSWORD,host=HOST, port=PORT)
    return conn



