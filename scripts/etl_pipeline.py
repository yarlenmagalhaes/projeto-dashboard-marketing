import pandas as pd
import os
from pathlib import Path # <-- 1. IMPORTAMOS A BIBLIOTECA

# --- 2. DEFINIMOS OS CAMINHOS ABSOLUTOS ---
PROJECT_DIR = Path(__file__).parent.parent
DATA_RAW_PATH = PROJECT_DIR / 'data_raw'
DATA_CLEAN_PATH = PROJECT_DIR / 'data_clean' # Pasta para os dados limpos

# Definimos os caminhos completos dos arquivos
GOOGLE_FILE = DATA_RAW_PATH / 'google_ads.csv'
FACEBOOK_FILE = DATA_RAW_PATH / 'facebook_ads.csv'
LINKEDIN_FILE = DATA_RAW_PATH / 'linkedin_ads.csv'

# --- PASSO 1: EXTRAÇÃO (EXTRACT) ---
try:
    df_google = pd.read_csv(GOOGLE_FILE)
    df_facebook = pd.read_csv(FACEBOOK_FILE)
    df_linkedin = pd.read_csv(LINKEDIN_FILE)
    print(f"Dados extraídos de '{DATA_RAW_PATH}' com sucesso!")
except FileNotFoundError as e:
    print(f"Erro: Arquivo não encontrado.")
    print(f"Detalhe: {e}")
    print("Verifique se você executou o 'gerador_de_dados.py' primeiro.")
    exit()

# --- PASSO 2: TRANSFORMAÇÃO (TRANSFORM) ---
print("Iniciando transformação dos dados...")

# (O restante do código de transformação não muda...)
# 2.1: Limpeza e Padronização
# --- GOOGLE ---
df_google_clean = df_google.rename(columns={
    'data': 'data',
    'custo_usd': 'custo',
    'cliques': 'cliques'
})
COTACAO_USD_BRL = 5.15
df_google_clean['custo'] = df_google_clean['custo'] * COTACAO_USD_BRL
df_google_clean['plataforma'] = 'Google Ads'
df_google_clean['impressoes'] = pd.NA

# --- FACEBOOK ---
df_facebook_clean = df_facebook.rename(columns={
    'date': 'data',
    'spend_brl': 'custo',
    'impressions': 'impressoes',
    'clicks': 'cliques'
})
df_facebook_clean['custo'] = df_facebook_clean['custo'] / 100
df_facebook_clean['data'] = pd.to_datetime(df_facebook_clean['data'], format='%d/%m/%Y')
df_facebook_clean['plataforma'] = 'Facebook Ads'

# --- LINKEDIN ---
df_linkedin_clean = df_linkedin.rename(columns={
    'dia': 'data',
    'valor_gasto': 'custo',
    'impressoes': 'impressoes'
})
df_linkedin_clean['data'] = pd.to_datetime(df_linkedin_clean['data'], format='%Y-%m-%d')
df_linkedin_clean['plataforma'] = 'LinkedIn Ads'
df_linkedin_clean['cliques'] = pd.NA

# 2.2: Consolidar Dados
df_consolidado = pd.concat([df_google_clean, df_facebook_clean, df_linkedin_clean], ignore_index=True)

# 2.3: Garantir Tipos de Dados Corretos
df_consolidado['data'] = pd.to_datetime(df_consolidado['data'])
df_consolidado['custo'] = df_consolidado['custo'].astype(float)
df_consolidado['impressoes'] = df_consolidado['impressoes'].astype('Int64')
df_consolidado['cliques'] = df_consolidado['cliques'].astype('Int64')

# 2.4: Engenharia de Features
df_consolidado['cpc'] = df_consolidado['custo'] / df_consolidado['cliques']
df_consolidado['cpm'] = (df_consolidado['custo'] / df_consolidado['impressoes']) * 1000

colunas_finais = [
    'data', 'plataforma', 'custo', 'cliques', 
    'impressoes', 'cpc', 'cpm'
]
df_consolidado = df_consolidado[colunas_finais]

# --- FIM DO ETL ---
print("Transformação concluída!")
print("\n--- Resultado do ETL (Dados Consolidados) ---")
print(df_consolidado.head(10)) # Mostra só os 10 primeiros
print(f"\nTotal de {len(df_consolidado)} registros processados.")

print("\n--- Informações do DataFrame Final ---")
df_consolidado.info()

# --- PASSO 3: LOAD (CARREGAMENTO) ---
# O caminho de saída agora também é absoluto e correto
OUTPUT_FILE = DATA_CLEAN_PATH / 'marketing_consolidado.csv' # <-- 3. ATUALIZADO

# Criar a pasta 'data_clean' se ela não existir
os.makedirs(DATA_CLEAN_PATH, exist_ok=True) # <-- 3. ATUALIZADO

df_consolidado.to_csv(OUTPUT_FILE, index=False)
print(f"\nDados limpos e consolidados salvos em '{OUTPUT_FILE}'")