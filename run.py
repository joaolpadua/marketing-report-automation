"""
run.py

Ponto de entrada da automação de relatórios de marketing.

Este script é responsável apenas por orquestrar o pipeline do sistema.
Ele não contém lógica de negócio complexa.

Fluxo do sistema:

1) carregar configurações
2) carregar clientes
3) buscar dados de campanhas
4) calcular métricas
5) gerar insights
6) montar relatório
7) enviar WhatsApp

O script é executado automaticamente via cron no Railway.
"""

# ---------------------------------------------------------------------
# Imports do projeto
# ---------------------------------------------------------------------

from src.config import Settings
from src.clients_sheets import load_clients_from_sheets

from src.data_providers.mock_provider import MockProvider

from src.report.metrics import aggregate_metrics
from src.report.insights import generate_insights
from src.report.formatter import build_whatsapp_report

from src.delivery.whatsapp_twilio import send_whatsapp_message_with_media

from src.utils.validation import validate_client


# ---------------------------------------------------------------------
# Imports padrão Python
# ---------------------------------------------------------------------

import logging
import datetime


# ---------------------------------------------------------------------
# Configuração global de logs
# ---------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Pipeline de processamento de um cliente
# ---------------------------------------------------------------------

def process_client(client, provider, settings):
    """
    Processa um cliente individual.

    Passos:
    1. validar dados do cliente
    2. buscar dados de campanhas
    3. calcular métricas
    4. gerar insights
    5. montar relatório
    6. enviar mensagem
    """

    logger.info(f"Processando cliente: {client['client_name']}")

    # validação básica do cliente
    validate_client(client)

    # buscar dados das campanhas (Mock ou Google Ads futuramente)
    campaign_data = provider.get_campaign_data(client)

    # calcular métricas agregadas
    metrics = aggregate_metrics(campaign_data)

    # gerar insights automáticos
    insights = generate_insights(metrics)

    # montar mensagem final
    message = build_whatsapp_report(client, metrics, insights)

    # enviar mensagem via WhatsApp
    send_whatsapp_message_with_media(
        account_sid=settings.twilio_account_sid,
        auth_token=settings.twilio_auth_token,
        from_whatsapp=settings.twilio_whatsapp_from,
        to_whatsapp=client["whatsapp_e164"],
        message=message,
        media_url=None,
    )

    logger.info(f"WhatsApp enviado para {client['client_name']}")


# ---------------------------------------------------------------------
# Função principal do job
# ---------------------------------------------------------------------

def main():
    """
    Executa o job completo de envio de relatórios.
    """

    start_time = datetime.datetime.utcnow()

    logger.info("===================================")
    logger.info("JOB AUTOMÁTICO DE RELATÓRIO INICIADO")
    logger.info(f"Início: {start_time}")
    logger.info("===================================")

    # carregar configurações do sistema
    settings = Settings.load()

    # carregar clientes da planilha
    clients = load_clients_from_sheets(settings.clients_sheet_url)

    logger.info(f"{len(clients)} clientes encontrados")

    # inicializar provider de dados
    # (mock por enquanto, Google Ads no futuro)
    provider = MockProvider()

    # processar cada cliente
    for client in clients:

        try:
            process_client(client, provider, settings)

        except Exception:
            # garante que erro em um cliente não interrompa o job
            logger.exception(
                f"Erro no cliente {client.get('client_name', 'desconhecido')}"
            )

    end_time = datetime.datetime.utcnow()

    logger.info("===================================")
    logger.info("JOB FINALIZADO")
    logger.info(f"Fim: {end_time}")
    logger.info(f"Duração: {end_time - start_time}")
    logger.info("===================================")


# ---------------------------------------------------------------------
# Execução direta do script
# ---------------------------------------------------------------------

if __name__ == "__main__":
    main()