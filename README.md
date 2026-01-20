# Sistema de Eventos

Sistema web para gerenciamento de eventos, permitindo cadastro, edição, visualização e controle de participantes e eventos de forma simples e organizada.

## 📌 Funcionalidades

* Cadastro de eventos
* Listagem de eventos
* Atualização e exclusão de eventos
* Gerenciamento de participantes
* Visualização de detalhes do evento

## 🛠️ Tecnologias Utilizadas

> Ajuste conforme o que você usou de verdade

* Python
* FastAPI / Flask / Django
* HTML / CSS / JavaScript
* Banco de Dados: SQLite / PostgreSQL / MySQL
* ORM: SQLAlchemy

## 📂 Estrutura do Projeto

```
sistema_eventos/
│-- app/
│   │-- main.py
│   │-- models/
│   │-- routes/
│   │-- schemas/
│   │-- database.py
│-- templates/
│-- static/
│-- requirements.txt
│-- README.md
```

## ⚙️ Como Rodar o Projeto

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/sistema_eventos.git
cd sistema_eventos
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Execute o projeto

```bash
uvicorn app.main:app --reload
```

Acesse em: `http://127.0.0.1:8000`

## 📌 Próximas Melhorias

* Autenticação de usuários
* Controle de permissões
* Exportação de eventos em PDF
* Dashboard administrativo
