import os
from dotenv import load_dotenv

base_dir = os.getcwd()
outer_dir = os.path.join(base_dir, "..")
outer_dir = os.path.abspath(outer_dir)
data_dir = os.path.join(outer_dir, 'data')
raw_data_dir = os.path.join(data_dir, 'raw')
processed_data_dir = os.path.join(data_dir, 'processed')
pnl_dir = os.path.join(processed_data_dir, 'pnl')
bal_dir = os.path.join(processed_data_dir, 'bal')
cf_dir =os.path.join(processed_data_dir, 'cf')

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

dsn = f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"