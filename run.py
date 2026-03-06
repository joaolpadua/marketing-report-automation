from src.config import Settings
from src.clients import load_clients
from src.data_providers.mock_provider import MockProvider
from src.report.pdf_report import build_pdf_report
from src.delivery.email_smtp import send_email_with_attachment
from src.delivery.whatsapp_twilio import send_whatsapp_message_with_media

def main():
    settings = Settings.load()
    clients = load_clients("clientes.csv")
    provider = MockProvider()

    for client in clients:
        print(f"\n=== Processando cliente: {client['client_name']} ===")

        metrics = provider.get_monthly_metrics(client)

        pdf_path = build_pdf_report(
            client=client,
            metrics=metrics,
            output_dir=settings.report_output_dir,
        )
        print(f"PDF gerado em: {pdf_path}")

        try:
            send_email_with_attachment(
                smtp_host=settings.smtp_host,
                smtp_port=settings.smtp_port,
                smtp_user=settings.smtp_user,
                smtp_pass=settings.smtp_pass,
                from_name=settings.email_from_name,
                from_email=settings.email_from,
                to_email=client["email"],
                subject=f"Relatório de Marketing - {metrics['period_label']} - {client['client_name']}",
                body=(
                    f"Olá, {client['client_name']}!\n\n"
                    f"Segue em anexo o relatório de marketing referente ao período {metrics['period_label']}.\n\n"
                    "Qualquer dúvida, estou à disposição."
                ),
                attachment_path=pdf_path,
            )
            print("Email enviado com sucesso ✅")
        except Exception as exc:
            print(f"Falha no envio de email ❌ -> {exc}")

        try:
            send_whatsapp_message_with_media(
                account_sid=settings.twilio_account_sid,
                auth_token=settings.twilio_auth_token,
                from_whatsapp=settings.twilio_whatsapp_from,
                to_whatsapp=client["whatsapp_e164"],
                message=f"Relatório de marketing {metrics['period_label']} gerado para {client['client_name']}",
                media_url=None,
            )
            print("WhatsApp enviado com sucesso ✅")

        except Exception as exc:
            print(f"Erro envio WhatsApp ❌ -> {exc}")


if __name__ == "__main__":
    main()