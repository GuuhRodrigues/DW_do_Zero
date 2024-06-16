import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)

def get_data():
    query= f"""
    SELECT
        *
    FROM
        public_datamart.dm_commodities;
    """

    df = pd.read_sql(query, engine)
    return df

st.set_page_config(page_title='Dashboard de Commidites', layout='wide')

st.title('Dashboard de Commodities')

st.write("""
Este dashboard mostra os dados de commodities e suas transações.
""")

df = get_data()

if df.empty:
    st.write("Não foi possível carregar os dados. Verifique se a tabela 'dm_commodities' existe no schema especificado.")
else:
    # Exibir os dados
    st.write("### Dados das Commodities")
    st.dataframe(df)

    # Resumo estatístico
    st.write("### Resumo Estatístico")
    st.write(df.describe())

    # Gráficos
    st.write("### Gráficos")

    # Gráfico de barras para ganhos e perdas
    st.bar_chart(df[['data', 'ganho']].set_index('data'))

    # Gráfico de linha para valores de fechamento
    st.line_chart(df[['data', 'valor_fechamento']].set_index('data'))