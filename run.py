"""
run.py

Ponto de entrada do sistema de automação de relatórios.

Este arquivo NÃO contém lógica de negócio.
Ele apenas orquestra o pipeline do sistema.

Pipeline:

carregar clientes
↓
buscar dados de campanhas
↓
calcular métricas
↓
gerar insights
↓
formatar relatório
↓
enviar WhatsApp
"""

from src.config import Settings
from src.clients_sheets import load_clients_from_sheets
from src.data_providers.mock_provider import MockProvider

from src.report.metrics import aggregate_metrics
from src.report.insights import generate_insights
from src.report.formatter import build_whatsapp_report

from src.delivery.whatsapp_twilio import send_whatsapp_message_with_media

from src.utils.validation import validate_client

import logging
import datetime


# -------------------------------------------------------------------------
# Configuração global de logs
# -------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------------
# Pipeline de processamento de um cliente
# -------------------------------------------------------------------------
def process_client(client, provider, settings):

    logger.info(f"Processando cliente: {client['client_name']}")

    # validação de dados do cliente
    validate_client(client)

    # buscar dados das campanhas
    campaign_data = provider.get_campaign_data(client)

    # calcular métricas consolidadas
    metrics = aggregate_metrics(campaign_data)

    # gerar insights automáticos
    insights = generate_insights(metrics)

    # gerar mensagem final
    message = build_whatsapp_report(client, metrics, insights)

    # enviar mensagem
    send_whatsapp_message_with_media(
        account_sid=settings.twilio_account_sid,
        auth_token=settings.twilio_auth_token,
        from_whatsapp=settings.twilio_whatsapp_from,
        to_whatsapp=client["whatsapp_e164"],
        message=message,
        media_url=None,
    )

    logger.info(f"WhatsApp enviado para {client['client_name']}")


# -------------------------------------------------------------------------
# Função principal do job
# -------------------------------------------------------------------------
def main():

    start_time = datetime.datetime.utcnow()

    logger.info("===================================")
    logger.info("JOB AUTOMÁTICO DE RELATÓRIO INICIADO")
    logger.info(f"Início: {start_time}")
    logger.info("===================================")

    settings = Settings.load()

    # carregar clientes da planilha
    clients = load_clients_from_sheets(settings.clients_sheet_url)

    logger.info(f"{len(clients)} clientes encontrados")

    # provider de dados
    provider = MockProvider()

    # processar clientes
    for client in clients:

        try:
            process_client(client, provider, settings)

        except Exception:
            logger.exception(f"Erro no cliente {client.get('client_name','desconhecido')}")

    end_time = datetime.datetime.utcnow()

    logger.info("===================================")
    logger.info("JOB FINALIZADO")
    logger.info(f"Fim: {end_time}")
    logger.info(f"Duração: {end_time - start_time}")
    logger.info("===================================")


# -------------------------------------------------------------------------
# Execução direta
# -------------------------------------------------------------------------
if __name__ == "__main__":
    main()