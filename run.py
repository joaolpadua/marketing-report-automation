from src.config import Settings
from src.clients_sheets import load_clients_from_sheets
from src.data_providers.mock_provider import MockProvider
from src.report.pdf_report import build_pdf_report
from src.delivery.email_resend import send_email_with_attachment
from src.delivery.whatsapp_twilio import send_whatsapp_message_with_media

import datetime


# -------------------------------------------------------------------------
# Agrega métricas de múltiplas campanhas em um único resumo.
#
# Esse processo simula o comportamento de ferramentas de marketing
# que consolidam diversas campanhas em um relatório único do cliente.
# -------------------------------------------------------------------------
def aggregate_metrics(campaign_data):

    impressions = sum(c["impressions"] for c in campaign_data)
    clicks = sum(c["clicks"] for c in campaign_data)
    cost = sum(c["cost"] for c in campaign_data)
    conversions = sum(c["conversions"] for c in campaign_data)

    # métricas derivadas
    ctr = (clicks / impressions * 100) if impressions else 0
    cpc = (cost / clicks) if clicks else 0
    cpa = (cost / conversions) if conversions else 0

    return {
        "period_label": "Últimos 30 dias",
        "impressions": impressions,
        "clicks": clicks,
        "cost_brl": round(cost, 2),
        "conversions": conversions,
        "ctr": round(ctr, 2),
        "cpc": round(cpc, 2),
        "cpa_brl": round(cpa, 2),
    }


# -------------------------------------------------------------------------
# Envio do relatório por email.
#
# A lógica fica isolada para facilitar troca futura de provedor
# (Resend, Sendgrid, SES, SMTP, etc).
# -------------------------------------------------------------------------
def send_email(client, metrics, pdf_path, settings):

    try:

        send_email_with_attachment(
            api_key=settings.resend_api_key,
            from_email=settings.email_from,
            to_email=client["email"],
            subject=f"Relatório de Marketing - {metrics['period_label']}",
            body=f"Olá {client['client_name']}, seu relatório está pronto.",
        )

        print("Email enviado com sucesso ✅")

    except Exception as exc:
        print(f"Falha no envio de email ❌ -> {exc}")


# -------------------------------------------------------------------------
# Monta mensagem resumida para envio via WhatsApp.
# -------------------------------------------------------------------------
def build_whatsapp_summary(client, metrics):

    return (
        f"📊 Relatório de Marketing\n\n"
        f"Cliente: {client['client_name']}\n"
        f"Período: {metrics['period_label']}\n\n"
        f"Cliques: {metrics['clicks']}\n"
        f"Impressões: {metrics['impressions']}\n"
        f"CTR: {metrics['ctr']}%\n"
        f"Custo: R$ {metrics['cost_brl']}\n"
        f"Conversões: {metrics['conversions']}\n"
        f"CPA: R$ {metrics['cpa_brl']}\n\n"
        f"📩 O relatório completo foi enviado por email."
    )


# -------------------------------------------------------------------------
# Envio de notificação via WhatsApp.
#
# Mantido separado para permitir adicionar outros canais no futuro
# (Slack, Telegram, SMS, etc).
# -------------------------------------------------------------------------
def send_whatsapp(client, metrics, settings):

    try:

        send_whatsapp_message_with_media(
            account_sid=settings.twilio_account_sid,
            auth_token=settings.twilio_auth_token,
            from_whatsapp=settings.twilio_whatsapp_from,
            to_whatsapp=client["whatsapp_e164"],
            message=build_whatsapp_summary(client, metrics),
            media_url=None,
        )

        print("WhatsApp enviado com sucesso ✅")

    except Exception as exc:
        print(f"Erro envio WhatsApp ❌ -> {exc}")


# -------------------------------------------------------------------------
# Pipeline de processamento para um único cliente.
#
# Fluxo:
#
# cliente
# ↓
# buscar dados de campanhas
# ↓
# consolidar métricas
# ↓
# gerar relatório PDF
# ↓
# enviar notificações
# -------------------------------------------------------------------------
def process_client(client, provider, settings):

    print(f"\n=== Processando cliente: {client['client_name']} ===")

    # 1. buscar dados de campanhas (mock do Google Ads)
    campaign_data = provider.get_campaign_data(client)

    # 2. consolidar métricas
    metrics = aggregate_metrics(campaign_data)

    # 3. gerar relatório PDF
    pdf_path = build_pdf_report(
        client=client,
        metrics=metrics,
        output_dir=settings.report_output_dir,
    )

    print(f"PDF gerado em: {pdf_path}")

    # 4. envio por email
    send_email(client, metrics, pdf_path, settings)

    # 5. envio de notificação WhatsApp
    send_whatsapp(client, metrics, settings)


# -------------------------------------------------------------------------
# Ponto de entrada da aplicação.
#
# Responsável por:
# - carregar configurações
# - carregar clientes
# - iniciar provider de dados
# - executar pipeline
# -------------------------------------------------------------------------
def main():

    start = datetime.datetime.utcnow()

    print("===================================")
    print("JOB AUTOMÁTICO DE RELATÓRIO")
    print("Início:", start)
    print("===================================")

    # carregar configurações do .env
    settings = Settings.load()

    # carregar clientes da planilha
    clients = load_clients_from_sheets(settings.clients_sheet_url)

    print(f"{len(clients)} clientes encontrados")

    # inicializar provider de dados (mock por enquanto)
    provider = MockProvider()

    # executar pipeline para cada cliente
    for client in clients:
        process_client(client, provider, settings)

    end = datetime.datetime.utcnow()

    print("===================================")
    print("JOB FINALIZADO")
    print("Fim:", end)
    print("Duração:", end - start)
    print("===================================")


# -------------------------------------------------------------------------
# Execução direta do script
# -------------------------------------------------------------------------
if __name__ == "__main__":
    main()