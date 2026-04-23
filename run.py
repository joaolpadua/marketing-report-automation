"""
Script principal do job automático de relatórios de marketing.

Responsável por:

1) Carregar configurações
2) Carregar lista de clientes
3) Buscar dados de campanhas
4) Agregar métricas
5) Comparar períodos
6) Gerar insights
7) Montar relatório
8) Enviar relatório via WhatsApp
9) Salvar relatório localmente
10) Registrar métricas de execução do job

Possui também modo seguro de execução:

python run.py --dry-run

Nesse modo o pipeline roda inteiro, mas o WhatsApp NÃO é enviado.
"""

import datetime
import logging
import argparse

from src.config import Settings
from src.data_sources import load_clients_from_sheets, MockProvider, GoogleAdsMCCProvider
from src.report import aggregate_metrics, compare_metrics, generate_insights, build_report
from src.delivery import send_whatsapp_message_with_media, save_report
from src.utils import validate_client, generate_run_id

# ---------------------------------------------------------
# Configuração básica de logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)





# --------------------------------------------------
# Envia mensagem WhatsApp
# --------------------------------------------------

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

def process_client(client, provider, settings, run_id, dry_run):
    """
    Executa todo o pipeline de geração de relatório para um cliente.
    """

    logger.info(f"Processando cliente: {client['client_name']}")

    # valida dados mínimos do cliente
    validate_client(client)

    # buscar dados de campanhas
    data = provider.get_campaign_data(client)

    current_data = data["current"]
    previous_data = data["previous"]

    # cálculo de métricas
    metrics_current = aggregate_metrics(current_data)
    metrics_previous = aggregate_metrics(previous_data)

    # comparação entre períodos
    comparison = compare_metrics(metrics_current, metrics_previous)

    # geração de insights
    insights = generate_insights(metrics_current, comparison)

    # construção da mensagem final
    message = build_report(
        client,
        metrics_current,
        comparison,
        insights
    )

    # -----------------------------------------------------
    # envio WhatsApp (bloqueado no modo dry-run)
    # -----------------------------------------------------

    if dry_run:

        logger.info(
            f"[DRY RUN] WhatsApp NÃO enviado para {client['client_name']}"
        )

    else:

        send_whatsapp(client, message, settings)

    # -----------------------------------------------------
    # persistência do relatório
    # -----------------------------------------------------

    save_report(run_id, client["client_name"], message)


# ---------------------------------------------------------
# Função principal do job
# ---------------------------------------------------------

def main():

    # -----------------------------------------------------
    # leitura de argumentos CLI
    # -----------------------------------------------------

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Executa pipeline sem enviar WhatsApp"
    )

    args = parser.parse_args()

    dry_run = args.dry_run

    # -----------------------------------------------------
    # início do job
    # -----------------------------------------------------

    start_time = datetime.datetime.utcnow()

    run_id = generate_run_id()

    logger.info(f"RUN ID: {run_id}")

    if dry_run:
        logger.info("MODO DRY RUN ATIVADO")

    logger.info("===================================")
    logger.info("JOB AUTOMÁTICO DE RELATÓRIO INICIADO")
    logger.info(f"Início: {start_time}")
    logger.info("===================================")

    # carregar configurações
    settings = Settings.load()

    print("USE_MOCK_DATA =", settings.use_mock_data)
    # carregar clientes
    clients = load_clients_from_sheets(settings.clients_sheet_url)

    logger.info(f"{len(clients)} clientes encontrados")

    # provider de dados
    if settings.use_mock_data:
        logger.info("Provider selecionado: MockProvider")
        provider = MockProvider()
    else:
        logger.info("Provider selecionado: GoogleAdsMCCProvider")
        provider = GoogleAdsMCCProvider(settings)

    # métricas de execução
    success_count = 0
    error_count = 0

    # -----------------------------------------------------
    # loop principal
    # -----------------------------------------------------

    for client in clients:

        try:

            process_client(
                client,
                provider,
                settings,
                run_id,
                dry_run
            )

            success_count += 1

        except Exception as exc:

            error_count += 1

            logger.exception(
                f"Erro no cliente {client.get('client_name')} -> {exc}"
            )

    # -----------------------------------------------------
    # finalização do job
    # -----------------------------------------------------

    end_time = datetime.datetime.utcnow()

    total = success_count + error_count

    logger.info("===================================")
    logger.info("JOB FINALIZADO")
    logger.info(f"Fim: {end_time}")
    logger.info(f"Duração total: {end_time - start_time}")

    logger.info(f"Clientes processados: {total}")
    logger.info(f"Sucesso: {success_count}")
    logger.info(f"Falhas: {error_count}")

    if total > 0:

        avg = (end_time - start_time).total_seconds() / total

        logger.info(f"Tempo médio por cliente: {round(avg, 2)}s")

    logger.info("===================================")


# ---------------------------------------------------------
# execução direta
# ---------------------------------------------------------

if __name__ == "__main__":
    main()