## Marketing Report Automation

Automação em Python para geração e envio automático de relatórios de marketing para múltiplos clientes.

O sistema lê uma lista de clientes, gera relatórios em PDF com métricas de performance e envia automaticamente os relatórios por email e WhatsApp.

Este projeto demonstra conceitos de:

. automação de processos

. integração com APIs

. geração de relatórios automatizados

. arquitetura modular em Python

## Arquitetura do Sistema

Fluxo geral do sistema:

```

clientes.csv
      ↓
carregamento de clientes
      ↓
data provider (fonte de métricas)
      ↓
geração de relatório PDF
      ↓
entrega automática
   • email (SMTP)
   • WhatsApp (Twilio API)

```

O sistema suporta múltiplos clientes, permitindo escalar facilmente apenas adicionando novas linhas no CSV.

## Estrutura do Projeto

```

marketing-report-automation/
│
├── clientes.csv
├── run.py
├── requirements.txt
├── .env.example
│
├── out/
│
└── src/
    │
    ├── config.py
    ├── clients.py
    │
    ├── data_providers/
    │     └── mock_provider.py
    │
    ├── report/
    │     └── pdf_report.py
    │
    └── delivery/
          ├── email_smtp.py
          └── whatsapp_twilio.py

```

## Tecnologias Utilizadas

Python

Pandas

ReportLab

SMTP

Twilio API

Requests

Python-dotenv

## Funcionalidades

✔ leitura de clientes via CSV
✔ geração automática de relatórios em PDF
✔ envio automático de relatórios por email
✔ envio automático de mensagens via WhatsApp
✔ suporte a múltiplos clientes
✔ arquitetura modular e escalável

## Instalação

Clone o repositório:

```

git clone https://github.com/joaolpadua/marketing-report-automation

```

Entre na pasta do projeto:

```

cd marketing-report-automation

```

Crie o ambiente virtual:

```

python -m venv .venv

```

Ative o ambiente virtual.

Windows:

```

.venv\Scripts\activate

```

Linux / Mac:

```

source .venv/bin/activate

```

Instale as dependências:

```

pip install -r requirements.txt

```

## Configuração

Crie um arquivo .env baseado no exemplo:

```
cp .env.example .env

```

Preencha com suas credenciais:

```

REPORT_OUTPUT_DIR=./out

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu_email@gmail.com
SMTP_PASS=sua_app_password
EMAIL_FROM_NAME=Seu Nome
EMAIL_FROM=seu_email@gmail.com

TWILIO_ACCOUNT_SID=seu_account_sid
TWILIO_AUTH_TOKEN=seu_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

```

## Base de Clientes

Clientes são definidos no arquivo:

```

clientes.csv

```

Exemplo:

```
client_id,client_name,email,whatsapp_e164
1,Cliente A,email@empresa.com,5511999999999
2,Cliente B,email@empresa.com,5511888888888

```

Para adicionar novos clientes basta inserir novas linhas no CSV.

## Execução

Execute o script:

```

python run.py

```

O sistema irá:

1 carregar clientes

2 gerar relatórios em PDF

3 enviar email

4 enviar mensagens via WhatsApp

## Exemplo de Saída

```

=== Processando cliente: Cliente A ===
PDF gerado em: ./out/relatorio_1_03-2026.pdf
Email enviado com sucesso
WhatsApp enviado com sucesso

=== Processando cliente: Cliente B ===
PDF gerado em: ./out/relatorio_2_03-2026.pdf
Email enviado com sucesso
WhatsApp enviado com sucesso

```

## Possíveis Evoluções

O projeto foi desenvolvido para ser facilmente expandido.

Possíveis evoluções incluem:

. integração com Google Ads API
. integração com Google Analytics GA4
. geração de gráficos no relatório
. armazenamento histórico de métricas
. dashboard analítico
. execução agendada automática
. deploy em Docker

## Objetivo do Projeto

Este projeto foi desenvolvido como demonstração prática de:

. automação de processos
. integração com APIs externas
. geração automatizada de relatórios
. arquitetura modular em Python
. pipelines simples de automação de dados