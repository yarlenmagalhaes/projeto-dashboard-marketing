import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from pathlib import Path # <-- 1. IMPORTAMOS A BIBLIOTECA

# --- 2. DEFINIMOS OS CAMINHOS ABSOLUTOS ---
# __file__ é o caminho deste script (gerador_de_dados.py)
# .parent vai para a pasta 'scripts/'
# .parent de novo vai para a pasta 'projeto_marketing_etl/'
PROJECT_DIR = Path(__file__).parent.parent 
# Agora, OUTPUT_DIR é um caminho completo e correto
OUTPUT_DIR = PROJECT_DIR / 'data_raw' 

# --- CONFIGURAÇÕES ---
NUM_REGISTROS_POR_FONTE = 300
DATA_INICIAL = datetime(2025, 1, 1)
DATA_FINAL = datetime(2025, 10, 31)

# Helper para gerar datas aleatórias
def gerar_datas_aleatorias(start, end, n):
    start_ts = int(start.timestamp())
    end_ts = int(end.timestamp())
    timestamps = np.random.randint(start_ts, end_ts, n)
    return [datetime.fromtimestamp(ts) for ts in timestamps]

print(f"Gerando {NUM_REGISTROS_POR_FONTE} registros para cada plataforma...")

# --- 3. CRIAR A PASTA DE SAÍDA ---
# Esta lógica agora usa o caminho absoluto e está correta
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"Diretório '{OUTPUT_DIR}' verificado/criado.")

# --- 1. Gerar Google Ads ---
datas = gerar_datas_aleatorias(DATA_INICIAL, DATA_FINAL, NUM_REGISTROS_POR_FONTE)
df_google = pd.DataFrame({
    'data': [d.strftime('%Y-%m-%d') for d in datas],
    'custo_usd': np.random.uniform(30.0, 250.0, NUM_REGISTROS_POR_FONTE).round(2),
    'cliques': np.random.randint(800, 7000, NUM_REGISTROS_POR_FONTE)
})
# Salva na pasta data_raw (agora com o caminho correto)
df_google.to_csv(OUTPUT_DIR / 'google_ads.csv', index=False) # <-- 4. CAMINHO ATUALIZADO
print("google_ads.csv gerado em 'data_raw/'.")

# --- 2. Gerar Facebook Ads ---
datas = gerar_datas_aleatorias(DATA_INICIAL, DATA_FINAL, NUM_REGISTROS_POR_FONTE)
df_facebook = pd.DataFrame({
    'date': [d.strftime('%d/%m/%Y') for d in datas],
    'spend_brl': np.random.randint(10000, 500000, NUM_REGISTROS_POR_FONTE),
    'impressions': np.random.randint(20000, 150000, NUM_REGISTROS_POR_FONTE),
    'clicks': np.random.randint(500, 3000, NUM_REGISTROS_POR_FONTE)
})
df_facebook.to_csv(OUTPUT_DIR / 'facebook_ads.csv', index=False) # <-- 4. CAMINHO ATUALIZADO
print("facebook_ads.csv gerado em 'data_raw/'.")

# --- 3. Gerar LinkedIn Ads ---
datas = gerar_datas_aleatorias(DATA_INICIAL, DATA_FINAL, NUM_REGISTROS_POR_FONTE)
df_linkedin = pd.DataFrame({
    'dia': [d.strftime('%Y-%m-%d') for d in datas],
    'valor_gasto': np.random.uniform(50.0, 400.0, NUM_REGISTROS_POR_FONTE).round(2),
    'impressoes': np.random.randint(5000, 30000, NUM_REGISTROS_POR_FONTE)
})
df_linkedin.to_csv(OUTPUT_DIR / 'linkedin_ads.csv', index=False) # <-- 4. CAMINHO ATUALIZADO
print("linkedin_ads.csv gerado em 'data_raw/'.")

print("\nNovos arquivos CSV gerados com sucesso!")          