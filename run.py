"""
run.py

Script principal do job automático de relatórios.

Responsável por:

1) Carregar configurações
2) Carregar lista de clientes
3) Buscar dados de campanhas
4) Agregar métricas
5) Comparar períodos
6) Gerar insights
7) Enviar relatório via WhatsApp
"""

import datetime
import logging

from src.config import Settings
from src.clients_sheets import load_clients_from_sheets
from src.data_providers.mock_provider import MockProvider
from src.report.metrics import aggregate_metrics
from src.report.comparison import compare_metrics
from src.report.insights import generate_insights
from src.delivery.whatsapp_twilio import send_whatsapp_message_with_media
from src.utils.validation import validate_client


# ---------------------------------------------------------
# Configuração básica de logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Monta mensagem final enviada ao cliente
# ---------------------------------------------------------

def build_whatsapp_summary(client, metrics, comparison, insights):
    """
    Constrói o texto final enviado ao cliente.
    """

    message = (
        f"📊 Relatório de Marketing\n\n"
        f"Cliente: {client['client_name']}\n"
        f"Período: Últimos 30 dias\n\n"

        f"Cliques: {metrics['clicks']} ({comparison['clicks_change']}%)\n"
        f"Impressões: {metrics['impressions']} ({comparison['impressions_change']}%)\n"
        f"CTR: {metrics['ctr']}%\n"
        f"Custo: R$ {metrics['cost_brl']}\n"
        f"Conversões: {metrics['conversions']} ({comparison['conversions_change']}%)\n"
        f"CPA: R$ {metrics['cpa_brl']} ({comparison['cpa_change']}%)\n"
    )

    if insights:
        message += "\n💡 Insights\n"

        for insight in insights:
            message += f"* {insight}\n"

    return message


# ---------------------------------------------------------
# Envia mensagem WhatsApp
# ---------------------------------------------------------

def send_whatsapp(client, message, settings):
    """
    Envia mensagem para o cliente via Twilio WhatsApp.
    """

    try:

        send_whatsapp_message_with_media(
            account_sid=settings.twilio_account_sid,
            auth_token=settings.twilio_auth_token,
            from_whatsapp=settings.twilio_whatsapp_from,
            to_whatsapp=client["whatsapp_e164"],
            message=message,
            media_url=None
        )

        logger.info(f"WhatsApp enviado para {client['client_name']}")

    except Exception as exc:

        logger.exception(
            f"Erro ao enviar WhatsApp para {client['client_name']} -> {exc}"
        )


# ---------------------------------------------------------
# Pipeline completo para um cliente
# ---------------------------------------------------------

def process_client(client, provider, settings):
    """
    Processa todo o fluxo de relatório para um único cliente.
    """

    logger.info(f"Processando cliente: {client['client_name']}")

    # valida dados mínimos do cliente
    validate_client(client)

    # buscar dados de campanhas
    data = provider.get_campaign_data(client)

    current_data = data["current"]
    previous_data = data["previous"]

    # calcular métricas
    metrics_current = aggregate_metrics(current_data)
    metrics_previous = aggregate_metrics(previous_data)

    # comparar períodos
    comparison = compare_metrics(metrics_current, metrics_previous)

    # gerar insights automáticos
    insights = generate_insights(metrics_current, comparison)

    # montar mensagem final
    message = build_whatsapp_summary(
        client,
        metrics_current,
        comparison,
        insights
    )

    # enviar relatório
    send_whatsapp(client, message, settings)


# ---------------------------------------------------------
# Função principal do job
# ---------------------------------------------------------

def main():

    start_time = datetime.datetime.utcnow()

    logger.info("===================================")
    logger.info("JOB AUTOMÁTICO DE RELATÓRIO INICIADO")
    logger.info(f"Início: {start_time}")
    logger.info("===================================")

    # carregar configurações
    settings = Settings.load()

    # carregar clientes
    clients = load_clients_from_sheets(settings.clients_sheet_url)

    logger.info(f"{len(clients)} clientes encontrados")

    # inicializar provider
    provider = MockProvider()

    # processar clientes
    for client in clients:

        try:

            process_client(client, provider, settings)

        except Exception as exc:

            logger.exception(
                f"Erro no cliente {client.get('client_name')} -> {exc}"
            )

    end_time = datetime.datetime.utcnow()

    logger.info("===================================")
    logger.info("JOB FINALIZADO")
    logger.info(f"Fim: {end_time}")
    logger.info(f"Duração: {end_time - start_time}")
    logger.info("===================================")


# ---------------------------------------------------------
# Execução direta do script
# ---------------------------------------------------------

if __name__ == "__main__":
    main()