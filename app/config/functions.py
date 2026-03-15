import streamlit as st
import pandas as pd
import pymongo
import config.db.mongo
from schemas import Campaign,Dataquality,Headers
import config.db.mongo
from schemas import Campaign
import json
import streamlit_antd_components as sac
import numpy as np
import ast
import bunnet as bn
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import io
from pygwalker.api.streamlit import StreamlitRenderer

# def get_campaigns_by_user(user):
#     client = st.session_state.mongo_client
#
#     bn.init_bunnet(database=client.info, document_models=[Campaign])
#     result = Campaign.find({"user_id":user}).to_list()
#     return result
#@st.cache_resource
def mongoexport(df, db_name, coll_name): # USANDO PYMONGO
    """Export a panda file from a mongo colection
    returns: panda data
    """
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db[coll_name]
    return pd.DataFrame(list(coll.find(projection={'_id': False}))) ## tirar o _id e limita para nao travar

def get_camaign_names(df,x_axis,y_axis):
    return sns.lineplot(data=df, x=x_axis, y=y_axis, markers=True)


def get_campaign_dq(db_name, id): # data quality
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Dataquality"]
    return pd.DataFrame(list(coll.find({"collection_id": id},projection={'_id': False}, limit=0)))  ## tirar o _id e limita para nao travar

def get_campaigns_by_user(user):
    client = st.session_state.mongo_client
    user = st.session_state.auth.user
    bn.init_bunnet(database=client.info, document_models=[Campaign])
    result = Campaign.find({"user_id":user}).to_list()

    return result

def delete_campaign(delete,collection_id):
    client = st.session_state.mongo_client
    user = st.session_state.auth.user
    db = client[user]
    db.drop_collection(collection_id)

    bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
    Headers.Headers.find(Headers.Headers.name == delete).delete().run()

    bn.init_bunnet(database=client[user], document_models=[Dataquality])
    Dataquality.find(Dataquality.name == delete).delete().run()

    bn.init_bunnet(database=client.info, document_models=[Campaign])
    Campaign.find_one(Campaign.name == delete).delete().run()

def get_header(db_name, id):
    client = st.session_state.mongo_client
    db = client[db_name]
    coll = db["Headers"]
    return pd.DataFrame(coll.find({"collection_id": id},projection={'_id': False}, limit=0))['header'][0]  ## tirar o _id e limita para nao travar

def upload_header(header,selected_campaign):
    if(header != None):
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
        dq = Headers.Headers(
                name=selected_campaign.name,
                user_id=selected_campaign.user_id,
                collection_id=selected_campaign.collection_id,
                header=header
            )
        dq.insert()
        return True #BaseException as e


def update_dataquality(data_quality,selected_campaign):
    try:
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        db = client[user]
        coll = db["Dataquality"]
        coll.update_one({"collection_id": selected_campaign}, {"$set": {"data": data_quality}})
        return True #BaseException as e
    except BaseException as e:
        print(e)
        return False

@st.cache_data
def download_campaign(_ds,ds_hd,tipo,range,user,campaign):

    for i in ds_hd.keys():
        _ds[i].attrs.update(ast.literal_eval(ds_hd[i]))  # .encode('utf-8'))

    # for var in _ds.variables:
    #     _ds[var].encoding.clear()

    memoria = io.BytesIO()
    compressao = dict(zlib=True, complevel=5)
    with zipfile.ZipFile(memoria, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        for dia, dataset in _ds.groupby("time.date"):
            if(dia >= range[0] and dia <= range[1]):
                if(tipo==".csv"):
                    pandas = dataset.to_pandas()
                    nome = f"{user}_{campaign}_{str(dia)}.csv"# USUARIO_CAMPANHA_DATA
                    arq = pandas.to_csv().encode('utf-8')
                elif(tipo==".cdf"):
                    #encoding = {var: compressao for var in dataset.data_vars}
                    nome = f"{user}_{campaign}_{str(dia)}.cdf"
                    arq =  dataset.to_netcdf()
                elif(tipo==".nc"):
                    #encoding = {var: compressao for var in dataset.data_vars}
                    nome = f"{user}_{campaign}_{str(dia)}.nc"
                    arq= dataset.to_netcdf()

                zf.writestr(nome, arq)
    return memoria.getvalue()

def upload_headers(variables,_columns,_selected_campaign):

    headers = {}
    for i in _columns:
        if (variables != None):
            headers.update({i: str(variables.mapping[i].attrs)})
        else:
            headers.update({i: "{}"})

    try:
        client = st.session_state.mongo_client
        user = st.session_state.auth.user
        bn.init_bunnet(database=client[user], document_models=[Headers.Headers])
        dq = Headers.Headers(
            name=_selected_campaign.name,
            user_id=_selected_campaign.user_id,
            collection_id=_selected_campaign.collection_id,
            header=headers
        )
        dq.insert()
        return True
    except BaseException as e:
        print(e)
        return False

def get_all_campaigns():
    client = st.session_state.mongo_client
    bn.init_bunnet(database=client.info, document_models=[Campaign])
    result = Campaign.find().to_list()

    return result

def export_campaign_to_parquet(user_id, campaign):
    """
    Exporta os dados da campanha para arquivo .parquet
    Retorna o caminho do arquivo gerado
    """
    try:
        client = st.session_state.mongo_client
        
        # Buscar dados da campanha
        df = mongoexport(None, user_id, campaign.collection_id)
        
        # Clean data before export - handle string 'NaN' values
        for col in df.columns:
            if df[col].dtype == 'object':
                # Replace string 'NaN' with actual NaN
                df[col] = df[col].replace('NaN', pd.NA)
                # Try to convert to numeric if possible
                df[col] = pd.to_numeric(df[col], errors='ignore')
    
        # Criar diretório de saída se não existir
        import os
        output_dir = "app/out/parquet"
        os.makedirs(output_dir, exist_ok=True)
        campaign_name = campaign.name.replace(" ", "_")
        # Nome do arquivo
        filename = f"{user_id}_{campaign_name}_{campaign.collection_id}.parquet"
        filepath = os.path.join(output_dir, filename)
        
        # Salvar como parquet
        df.to_parquet(filepath, index=False, compression='snappy')
        
        return filepath, filename
    except Exception as e:
        print(f"Erro ao exportar para parquet: {e}")
        return None, None

def generate_jupyter_code(base_url, filename, campaign_name):
    """
    Gera um arquivo .ipynb próprio para Jupyter Notebook e Google Colab
    """

    
    # Estrutura do notebook Jupyter
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# 📊 Análise da Campanha: {campaign_name}\n",
                    "### Gerado automaticamente pelo DataQualityDataMap\n",
                    "\n",
                    "Este notebook contém o código necessário para carregar e analisar os dados da campanha."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📦 Instalação de Dependências\n",
                    "Execute esta célula apenas se estiver no Google Colab ou se precisar instalar as bibliotecas."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Descomente as linhas abaixo se necessário\n",
                    "# !pip install pandas numpy matplotlib seaborn pyarrow"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📚 Importação de Bibliotecas"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "\n",
                    "# Configurações de visualização\n",
                    "sns.set_palette('husl')\n",
                    "%matplotlib inline"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🔗 Carregamento dos Dados"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"# URL do arquivo parquet no servidor\n",
                    f"parquet_url = \"{base_url}/out/parquet/{filename}\"\n",
                    "\n",
                    "# Carregar os dados\n",
                    "print(\"Carregando dados...\")\n",
                    "df = pd.read_parquet(parquet_url)\n",
                    "print(f\"✅ Dados carregados com sucesso! Shape: {df.shape}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🔍 Visualização Inicial dos Dados"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Informações básicas\n",
                    "print(\"=\"*50)\n",
                    "print(\"INFORMAÇÕES DO DATASET\")\n",
                    "print(\"=\"*50)\n",
                    "print(f\"Shape dos dados: {df.shape}\")\n",
                    "print(f\"Número de linhas: {df.shape[0]:,}\")\n",
                    "print(f\"Número de colunas: {df.shape[1]}\")\n",
                    "print(\"\\nPrimeiras linhas:\")\n",
                    "df.head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Informações das colunas\n",
                    "print(\"\\nInformações das colunas:\")\n",
                    "df.info()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📈 Estatísticas Descritivas"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Estatísticas descritivas\n",
                    "df.describe()"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🔎 Análise de Qualidade dos Dados"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Verificar valores nulos\n",
                    "print(\"Valores nulos por coluna:\")\n",
                    "null_counts = df.isnull().sum()\n",
                    "null_percentages = (null_counts / len(df) * 100).round(2)\n",
                    "\n",
                    "null_df = pd.DataFrame({\n",
                    "    'Valores Nulos': null_counts,\n",
                    "    'Percentual (%)': null_percentages\n",
                    "})\n",
                    "null_df = null_df[null_df['Valores Nulos'] > 0].sort_values('Valores Nulos', ascending=False)\n",
                    "\n",
                    "if len(null_df) > 0:\n",
                    "    print(null_df)\n",
                    "else:\n",
                    "    print(\"✅ Nenhum valor nulo encontrado!\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 📊 Visualizações"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Visualizar valores nulos\n",
                    "if len(null_df) > 0:\n",
                    "    plt.figure(figsize=(12, 6))\n",
                    "    null_df['Percentual (%)'].plot(kind='barh', color='coral')\n",
                    "    plt.xlabel('Percentual de Valores Nulos (%)')\n",
                    "    plt.title('Distribuição de Valores Nulos por Coluna')\n",
                    "    plt.tight_layout()\n",
                    "    plt.show()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Matriz de correlação (apenas para colunas numéricas)\n",
                    "numeric_cols = df.select_dtypes(include=[np.number]).columns\n",
                    "\n",
                    "if len(numeric_cols) > 1:\n",
                    "    plt.figure(figsize=(12, 10))\n",
                    "    correlation_matrix = df[numeric_cols].corr()\n",
                    "    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0)\n",
                    "    plt.title('Matriz de Correlação')\n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "else:\n",
                    "    print(\"Não há colunas numéricas suficientes para matriz de correlação.\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 🎯 Suas Análises Personalizadas\n",
                    "\n",
                    "Use as células abaixo para realizar suas próprias análises!"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Exemplo: Plotar uma coluna específica\n",
                    "# Substitua 'nome_da_coluna' pelo nome real da coluna que deseja analisar\n",
                    "\n",
                    "# df['nome_da_coluna'].plot(figsize=(15, 6))\n",
                    "# plt.title('Análise de nome_da_coluna')\n",
                    "# plt.ylabel('Valores')\n",
                    "# plt.xlabel('Índice')\n",
                    "# plt.show()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Sua análise aqui\n"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.6"
            },
            "colab": {
                "name": f"Analise_{campaign_name}.ipynb",
                "provenance": []
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    
    # Retornar como string JSON formatada
    return json.dumps(notebook, indent=2, ensure_ascii=False)


def update_campaign_info(campaign_id, updated_data):
    """
    Atualiza as informações de uma campanha no banco de dados

    Args:
        campaign_id: ID da campanha a ser atualizada
        updated_data: Dicionário com os dados a serem atualizados

    Returns:
        bool: True se sucesso, False se falha
    """
    try:
        client = st.session_state.mongo_client
        bn.init_bunnet(database=client.info, document_models=[Campaign])

        # Usar update direto via MongoDB
        from bson import ObjectId
        
        # Preparar os dados para atualização
        update_fields = {}
        if 'name' in updated_data:
            update_fields['name'] = updated_data['name']
        if 'description' in updated_data:
            update_fields['description'] = updated_data['description']
        if 'date' in updated_data:
            update_fields['date'] = updated_data['date']
        if 'public' in updated_data:
            update_fields['public'] = updated_data['public']
        if 'validated' in updated_data:
            update_fields['validated'] = updated_data['validated']

        # Atualizar usando update_one do pymongo diretamente
        db = client.info
        collection = db['Campaign']  # Nome da coleção (ajuste se necessário)
        
        result = collection.update_one(
            {'_id': ObjectId(campaign_id)},
            {'$set': update_fields}
        )

        if result.modified_count > 0:
            return True
        elif result.matched_count > 0:
            # Documento encontrado mas não modificado (valores iguais)
            return True
        else:
            print(f"Campanha não encontrada: {campaign_id}")
            return False

    except Exception as e:
        print(f"Erro ao atualizar campanha: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_campaign_info(campaign):
    """
    Retorna as informações de uma campanha formatadas

    Args:
        campaign: Objeto Campaign

    Returns:
        dict: Dicionário com as informações da campanha
    """
    return {
        'name': campaign.name,
        'description': campaign.description,
        'date': campaign.date,
        'public': campaign.public,
        'validated': campaign.validated,
        'user_id': campaign.user_id,
        'collection_id': campaign.collection_id
    }