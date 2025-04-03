import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from datetime import datetime

def salvar_mysql(df):
    load_dotenv()
    host = 'localhost'
    port = '3306'
    user = os.getenv("MYSQL_USER")
    senha = quote_plus(os.getenv("MYSQL_PASSWORD"))
    database_name = 'db_imoveis'

    DATABASE_URL = f'mysql+pymysql://{user}:{senha}@{host}:{port}/{database_name}'
    engine = create_engine(DATABASE_URL)

    df['data_extracao'] = datetime.now()

    try:
        with engine.begin() as connection:
            links_existentes = pd.read_sql('SELECT link FROM imoveis', con=connection)['link'].tolist()
            novos_df = df[~df['link'].isin(links_existentes)]

            if not novos_df.empty:
                novos_df.to_sql(name='imoveis', con=connection, if_exists='append', index=False)
                print(f"{len(novos_df)} novos registros inseridos no banco.")
            else:
                print("Nenhum novo registro para inserir (todos já estavam no banco).")

    except Exception as e:
        print("Erro ao inserir no banco:", e)