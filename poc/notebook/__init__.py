import os
from dotenv import load_dotenv

base_dir = os.getcwd()

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user_super = os.getenv('DB_USER')
db_password_super = os.getenv('DB_PASSWORD')

db_connection_string_super = f"host {db_host} port {db_port} user {db_user_super} password {db_password_super}"