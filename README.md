# Monitor de Infraestrutura

  Sistema de monitoramento de serviços de rede com dashboard web em tempo real.

## Sobre o projeto

Aplicação web que monitora automaticamente a disponibilidade e latência de serviços HTTP e TCP, armazena histórico de resultados e exibe tudo em um dashboard atualizado a cada 30 segundos.
Funcionalidades

  - Cadastro de serviços para monitorar (HTTP e TCP)
  - Monitoramento automático a cada 1 minuto
  - Histórico de checks com latência e status
  - Dashboard web com status em tempo real
  - API REST documentada automaticamente

## Tecnologias

  - **Python 3.12**
  - **FastAPI**
  - **SQLAlchemy** — ORM para banco de dados
  - **APScheduler** — agendamento de tarefas
  - **httpx** — cliente HTTP assíncrono
  - **SQLite** — banco de dados local

## Como rodar localmente (no Linux)

**Pré-requisitos:** Python 3.10+
```bash
# Clone o repositório
git clone https://github.com/limati2001/Sistema-de-Monitoramento-de-Infraestrutura-com-Dashboard-Web
cd Sistema-de-Monitoramento-de-Infraestrutura-com-Dashboard-Web

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env

# Inicie a aplicação
uvicorn app.main:app --reload
```

Acesse:
- **Dashboard:** http://localhost:8000/api/dashboard/
- **API Docs:** http://localhost:8000/docs

## Endpoints principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | /api/services/ | Lista serviços cadastrados |
| POST | /api/services/ | Cadastra novo serviço |
| DELETE | /api/services/{id} | Remove serviço |
| GET | /api/monitor/{id} | Checa serviço manualmente |
| GET | /api/monitor/{id}/history | Histórico de checks |
| GET | /api/dashboard/ | Dashboard web |
