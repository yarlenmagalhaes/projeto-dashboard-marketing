# 🚀 Projeto: Dashboard de Análise de Marketing Digital (ETL + Streamlit)

Este projeto simula um pipeline de dados completo, desde a extração de dados brutos de múltiplas fontes até a apresentação em um dashboard interativo para análise de negócios.

### ✨ [Clique aqui para ver o Dashboard ao vivo!](https://projeto-dashboard-marketing.streamlit.app/) ✨

---

### 📊 Visão Geral do Dashboard

Aqui está uma prévia da aplicação em funcionamento:

![Prévia do Dashboard](https://github.com/yarlenmagalhaes/projeto-dashboard-marketing/issues/1#issue-3581571676)

---

### 📖 Sobre o Projeto

O desafio deste projeto era consolidar dados de performance de marketing de três plataformas distintas (Google Ads, Facebook Ads, LinkedIn Ads) em uma única fonte de verdade.

O processo foi dividido em duas grandes etapas:

1.  **Engenharia de Dados (ETL):**
    * **Extração (Extract):** Os scripts simulam a extração de dados brutos (`.csv` sujos e com formatos diferentes) de cada plataforma.
    * **Transformação (Transform):** Usando Python e Pandas, os dados são limpos, padronizados (datas, moedas), unificados e enriquecidos com novas métricas de negócio (como CPC e CPM).
    * **Carga (Load):** O resultado final é um único arquivo (`.csv` limpo) salvo na pasta `data_clean/`, pronto para o consumo.

2.  **Análise e Visualização (BI):**
    * Um dashboard interativo foi construído com Streamlit para consumir o arquivo de dados limpos.
    * Ele permite que um "gestor" filtre os dados por plataforma e período.
    * Exibe KPIs centrais (Custo Total, Cliques, Impressões, CPC/CPM Médio).
    * Apresenta gráficos de série temporal e de distribuição de custos para facilitar a tomada de decisão.

---

### 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem principal do projeto.
* **Pandas:** Para todo o processo de ETL (limpeza, transformação e manipulação dos dados).
* **Streamlit:** Para a construção do dashboard web interativo.
* **Plotly:** Para a criação dos gráficos interativos.
* **Git & GitHub:** Para versionamento de código e deploy.
* **Streamlit Community Cloud:** Para a hospedagem (deploy) da aplicação.

---

### 🏃‍♂️ Como Rodar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/yarlenmagalhaes/projeto-dashboard-marketing.git](https://github.com/yarlenmagalhaes/projeto-dashboard-marketing.git)
    cd projeto-dashboard-marketing
    ```

2.  **Crie um ambiente virtual (opcional, mas recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o pipeline de ETL primeiro:**
    (Isso irá criar a pasta `data_clean/` com os dados necessários)
    ```bash
    python scripts/etl_pipeline.py
    ```

5.  **Execute o dashboard:**
    ```bash
    streamlit run dashboard.py
    ```
    (O app abrirá automaticamente no seu navegador!)