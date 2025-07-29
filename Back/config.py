import psycopg2
from dotenv import load_dotenv
import os
import bcrypt

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def connect_db():
    # Conectar a la base de datos PostgreSQL usando las variables de entorno
    try:
        conn= None
        cur= None
        conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=os.getenv("PORT"),
            dbname=os.getenv("DBNAME")
        )
        conexion = True
        # Crear un cursor para ejecutar consultas
        cur = conn.cursor()
        error = None
        return conn, cur, conexion, error
    except Exception as e:
        print(f"Failed to connect: {e}")
        conexion = False
        error = str(e)
        return None, None, conexion, error
    
def verify_password(stored_password, provided_password):
    #convertir los tipos de datos si es necesario
    if isinstance(stored_password, str):
        stored_password = bytes.fromhex(stored_password.replace('\\x',''))
    if isinstance(provided_password, str):
        provided_password = provided_password.encode('utf-8')
    return bcrypt.checkpw(provided_password, stored_password)