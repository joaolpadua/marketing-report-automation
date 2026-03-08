Marketing Report Automation

Automação em Python para geração e envio automático de relatórios de
marketing para múltiplos clientes.

O sistema lê uma base de clientes, coleta métricas de campanhas, gera
relatórios em PDF e envia automaticamente os resultados por email e
WhatsApp.

Este projeto demonstra conceitos reais de engenharia de software
aplicados a automação de marketing, incluindo integração com APIs,
arquitetura modular e execução em nuvem.

Principais conceitos aplicados

-   automação de processos
-   integração com APIs externas
-   geração automatizada de relatórios
-   arquitetura modular em Python
-   execução automatizada em cloud

------------------------------------------------------------------------

Problema

Agências de marketing frequentemente precisam gerar relatórios
periódicos para dezenas de clientes.

Esse processo normalmente envolve:

-   coletar métricas manualmente
-   montar relatórios
-   enviar por email
-   comunicar resultados aos clientes

Esse fluxo consome tempo operacional e dificulta escalar o atendimento.

------------------------------------------------------------------------

Solução

Este projeto automatiza completamente esse processo.

```

Fluxo do sistema:

    Google Sheets (lista de clientes)
            ↓
    Python Runner
            ↓
    Data Provider (fonte de métricas)
            ↓
    Geração de relatório em PDF
            ↓
    Entrega automática
       • Email (Resend API)
       • WhatsApp (Twilio API)
            ↓
    Execução automática via cron em cloud

```
O sistema suporta múltiplos clientes e pode escalar facilmente apenas adicionando novas linhas na planilha.

------------------------------------------------------------------------

Arquitetura do Sistema

```
Fluxo geral:

    Base de clientes (Google Sheets)
            ↓
    Carregamento de clientes
            ↓
    Data Provider (fonte de métricas)
            ↓
    Agregação de métricas
            ↓
    Geração de relatório PDF
            ↓
    Entrega automática
       • Email (Resend API)
       • WhatsApp (Twilio API)

```
A arquitetura foi projetada para permitir substituição fácil da fonte de dados, como por exemplo integrar diretamente com a Google Ads API no futuro.

------------------------------------------------------------------------

Estrutura do Projeto

```
    marketing-report-automation/

    ├── run.py
    ├── requirements.txt
    ├── runtime.txt
    ├── .env.example
    │
    ├── out/
    │
    └── src/
        ├── config.py
        ├── clients_sheets.py
        │
        ├── data_providers/
        │     ├── mock_provider.py
        │     └── google_ads_provider.py
        │
        ├── report/
        │     └── pdf_report.py
        │
        └── delivery/
              ├── email_resend.py
              └── whatsapp_twilio.py

```

------------------------------------------------------------------------

Tecnologias Utilizadas

-   Python
-   Pandas
-   ReportLab
-   Requests
-   Twilio API
-   Resend Email API
-   Google Sheets (CSV export)
-   Python-dotenv
-   Railway (deploy em cloud)

------------------------------------------------------------------------

Funcionalidades

✔ leitura de clientes via Google Sheets
✔ geração automática de relatórios em PDF
✔ envio automático de relatórios por email
✔ envio automático de mensagens via WhatsApp
✔ suporte a múltiplos clientes
✔ arquitetura modular e escalável
✔ execução automatizada em nuvem

------------------------------------------------------------------------

Instalação

Clone o repositório

    git clone https://github.com/joaolpadua/marketing-report-automation

Entre na pasta do projeto

    cd marketing-report-automation

Crie o ambiente virtual

    python -m venv .venv

Ative o ambiente virtual

Windows

    .venv\Scripts\activate

Linux / Mac

    source .venv/bin/activate

Instale as dependências

    pip install -r requirements.txt

------------------------------------------------------------------------

Configuração

Crie um arquivo .env baseado no exemplo

    cp .env.example .env

Preencha com suas credenciais

    REPORT_OUTPUT_DIR=./out

    CLIENTS_SHEET_URL=url_da_planilha_csv

    RESEND_API_KEY=sua_api_key

    EMAIL_FROM_NAME=Relatórios
    EMAIL_FROM=onboarding@resend.dev

    TWILIO_ACCOUNT_SID=seu_account_sid
    TWILIO_AUTH_TOKEN=seu_auth_token
    TWILIO_WHATSAPP_FROM=whatsapp:+14155238886

------------------------------------------------------------------------

Base de Clientes

Clientes são definidos em uma planilha Google Sheets publicada como CSV.

Exemplo de estrutura:

    client_id,client_name,email,whatsapp_e164,active
    1,Cliente A,email@empresa.com,5511999999999,TRUE
    2,Cliente B,email@empresa.com,5511888888888,TRUE

Para adicionar novos clientes basta inserir novas linhas na planilha.

------------------------------------------------------------------------

Execução

Execute o script

    python run.py

O sistema irá automaticamente:

1.  carregar clientes da planilha
2.  coletar métricas
3.  gerar relatórios em PDF
4.  enviar relatórios por email
5.  enviar resumo via WhatsApp

------------------------------------------------------------------------

Exemplo de Saída

    === Processando cliente: Cliente A ===
    PDF gerado em: ./out/relatorio_1_Últimos 30 dias.pdf
    Email enviado com sucesso
    WhatsApp enviado com sucesso

    === Processando cliente: Cliente B ===
    PDF gerado em: ./out/relatorio_2_Últimos 30 dias.pdf
    Email enviado com sucesso
    WhatsApp enviado com sucesso

------------------------------------------------------------------------

Execução Automática

O projeto pode ser executado automaticamente em cloud usando cron jobs.

Exemplo de agendamento semanal:

    0 8 * * 1

segunda-feira às 08:00

------------------------------------------------------------------------

Possíveis Evoluções

-   integração direta com Google Ads API
-   integração com Google Analytics GA4
-   geração de gráficos no relatório
-   armazenamento histórico de métricas
-   dashboard analítico
-   paralelização para centenas de clientes
-   containerização com Docker

------------------------------------------------------------------------

Objetivo do Projeto

Este projeto foi desenvolvido como demonstração prática de:

-   automação de processos
-   integração com APIs externas
-   geração automatizada de relatórios
-   arquitetura modular em Python
-   pipelines simples de automação de dados
-   deploy e execução automatizada em cloud
