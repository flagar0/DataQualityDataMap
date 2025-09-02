# DataQualityDataMap

Uma plataforma digital para controle de qualidade de dados desenvolvida com Streamlit, oferecendo uma interface web intuitiva para gerenciamento de campanhas de dados, análise de qualidade e visualização de dados.

## 📋 Descrição

O DataQualityDataMap é um sistema completo de gerenciamento de dados que permite aos usuários:

- **Criar e gerenciar campanhas de dados** com controle de qualidade
- **Fazer upload de dados** em formatos CSV, TSV, CDF e NetCDF
- **Analisar a qualidade dos dados** com timeline visual interativa
- **Visualizar dados** através de gráficos e estatísticas
- **Exportar dados** em diferentes formatos
- **Acessar campanhas públicas** sem necessidade de login

## ✨ Funcionalidades Principais

### 🔐 Sistema de Autenticação
- Login seguro com MongoDB
- Acesso público a campanhas compartilhadas
- Controle de usuários e permissões

### 📊 Gerenciamento de Campanhas
- **Criar**: Defina novas campanhas com nome, descrição e período
- **Editar**: Modifique cabeçalhos e relatórios de qualidade
- **Gerenciar**: Faça upload de dados e configure instrumentos
- **Visualizar**: Explore dados com gráficos interativos

### 📈 Controle de Qualidade de Dados
- **Timeline Visual**: Interface interativa para marcar períodos de qualidade
- **Códigos de Cores**: 
  - 🟢 Verde: Dados OK
  - 🔴 Vermelho: Dados ausentes
  - 🟡 Amarelo: Dados suspeitos
  - ⚪ Branco: Notas
  - ⚫ Preto: Dados incorretos
- **Análise Automática**: Detecção automática de dados ausentes

### 📊 Visualização de Dados
- **Gráficos Interativos**: Scatter plots, box plots, histogramas
- **Estatísticas Descritivas**: Resumos estatísticos dos dados
- **Análise de Valores Ausentes**: Identificação de lacunas nos dados
- **Explorador Interativo**: Interface PyGWalker para análise avançada

### 💾 Exportação de Dados
- **Formatos Suportados**: CSV, CDF, NetCDF
- **Seleção de Período**: Exporte dados por intervalo de tempo
- **Compressão ZIP**: Download em arquivo compactado

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- MongoDB (local ou Atlas)

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/DataQualityDataMap.git
   cd DataQualityDataMap
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure o banco de dados**
   - Configure a conexão MongoDB em `app/config/db/mongo.py`
   - Ou use o MongoDB Atlas (configurado por padrão)

## 🏃‍♂️ Como Executar

### Desenvolvimento Local
```bash
streamlit run app/app.py
```

### Produção
```bash
streamlit run app/app.py --server.enableXsrfProtection false
```

O aplicativo estará disponível em `http://localhost:8501`

## 📁 Estrutura do Projeto

```
DataQualityDataMap/
├── app/
│   ├── components/          # Componentes reutilizáveis
│   │   ├── contact/         # Componentes de contato
│   │   └── location/        # Componentes de localização
│   ├── config/              # Configurações do sistema
│   │   ├── auth.py          # Autenticação
│   │   ├── db/              # Configuração do banco
│   │   └── functions.py     # Funções utilitárias
│   ├── layouts/             # Layouts das páginas
│   │   ├── campaign_create/ # Criação de campanhas
│   │   ├── campaign_edit/   # Edição de campanhas
│   │   ├── campaign_manage/ # Gerenciamento de campanhas
│   │   ├── campaign_view/   # Visualização de campanhas
│   │   └── login/           # Página de login
│   ├── pages/               # Páginas do Streamlit
│   ├── schemas/             # Modelos de dados
│   ├── utils/               # Utilitários
│   └── app.py               # Aplicação principal
├── testes/                  # Testes e scripts
├── requirements.txt         # Dependências Python
├── LICENSE                  # Licença MIT
└── README.md               # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Frontend**: Streamlit, Streamlit Antd Components
- **Backend**: Python, PyMongo, Beanie (ODM)
- **Banco de Dados**: MongoDB
- **Visualização**: Matplotlib, Seaborn, PyGWalker
- **Processamento de Dados**: Pandas, Xarray
- **Timeline**: Streamlit Timeline

## 📊 Formatos de Dados Suportados

- **CSV**: Arquivos de valores separados por vírgula
- **TSV**: Arquivos de valores separados por tabulação
- **CDF**: Common Data Format
- **NetCDF**: Network Common Data Form

## 🔧 Configuração

### Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
MONGODB_URI=mongodb+srv://usuario:senha@cluster.mongodb.net/
DETA_KEY=sua_chave_deta
```

### Configuração do MongoDB
Edite `app/config/db/mongo.py` para configurar sua conexão MongoDB:

```python
MongoClient("mongodb+srv://usuario:senha@cluster.mongodb.net/")
```

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!


