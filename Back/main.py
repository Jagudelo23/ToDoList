from fastapi import FastAPI, Request
import json
from fastapi.responses import JSONResponse
import jwt
import logging
from config import connect_db, verify_password
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Configuración básica del logger
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/Login")
async def Login(request: Request):
    logger.info("Se llamó a la función Login")
    conn = None
    try:
        EXPIRACION = timedelta(minutes=30)  # Definir la expiración del token
        SECRETO =os.getenv("SECRETO")  
        #Extracción de parametros de la petición
        body = await Request.json()
        user = body.get("user")
        password = body.get("password")

        # Validación de los parámetros
        logger.info(f"Usuario: {user}, Contraseña: {password}")
        if not user or not password:
            logger.error("Faltan credenciales de usuario o contraseña")
            return JSONResponse(status_code=400, content={"error": "Faltan credenciales de usuario o contraseña"})
        
        # Busqueda del usuario en la base de datos
        conn, cur, conexion, error = connect_db()

            # Verificación de la conexión a la base de datos
        if conexion == False:
            logger.error(error)
            return JSONResponse(status_code=500, content={"error": error})
        
        cur.execute("SELECT * FROM users WHERE username = %s", (user,))
        result = cur.fetchone()

        # Verificación contraseña
        if result:
            logger.info("Usuario encontrado en la base de datos")
            if verify_password(result[1], password):
                logger.info("Contraseña verificada correctamente")
                # Generación del token JWT
                token = jwt.encode({
                    'user_id': result[0],
                    'username': result[1],
                    'exp':datetime.utcnow()+EXPIRACION # Definir la expiración del token
                }, SECRETO, algorithm='HS256')
                logger.info("Token JWT generado correctamente")
                return JSONResponse(status_code=200, content={"token": token})
            else:
                logger.error("Contraseña incorrecta")
                return JSONResponse(status_code=401, content={"error": "Contraseña incorrecta"})
        else:
            logger.error("Usuario no encontrado")
            return JSONResponse(status_code=404, content={"error": "Usuario no encontrado"})
    except Exception as e:
        # Manejo de errores inesperados
        logger.error(f"Error en la función Login: {str(e)}")
        return JSONResponse(status_code=500, content={"error": "Error interno del servidor"})
    finally:
        # Cierre de la conexion a la base de datos
        if conn:
            conn.close()
            logger.info("Conexión a la base de datos cerrada")
        logger.info("Finalizando la función Login")