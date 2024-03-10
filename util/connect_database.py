import psycopg2
import os

from dotenv import load_dotenv

def connect_to_database():
    load_dotenv()
    return psycopg2.connect(os.getenv('DB_URL'))