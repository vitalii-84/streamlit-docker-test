import pandas as pd
from sqlalchemy import create_engine
import os


# Отримайте URL бази даних
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://your_user:your_password@localhost:5432/your_database')

db = create_engine(DATABASE_URL)
conn = db.connect()

files = ['brands', 'categories', 'customers', 'order_items', 'orders', 'products', 'staffs', 'stocks', 'stores']

for file in files:
    df = pd.read_csv(f'/csv_files/{file}.csv')
    df.to_sql(file, con=conn, if_exists='replace', index=False)
