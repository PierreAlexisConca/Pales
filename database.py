import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

# Cargar .env
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": "utf8mb4"
}

# Crear pool de conexiones
connection_pool = pooling.MySQLConnectionPool(
    pool_name="palees_pool",
    pool_size=5,
    **DB_CONFIG
)

def get_conn():
    """Devuelve una conexión desde el pool."""
    return connection_pool.get_connection()
