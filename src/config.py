from dataclasses import dataclass
from dotenv import load_dotenv
import os


# -------------------------------------------------------------------------
# Classe de configuração central do sistema.
#
# Responsável por carregar todas as variáveis de ambiente (.env ou cloud)
# e disponibilizar essas configurações para o restante da aplicação.
#
# Isso evita "espalhar" os.getenv() pelo código inteiro.
# -------------------------------------------------------------------------
@dataclass
class Settings:

    def __init__(
        self,
        report_output_dir,
        smtp_host,
        smtp_port,
        smtp_user,
        smtp_pass,
        email_from_name,
        email_from,
        twilio_account_sid,
        twilio_auth_token,
        twilio_whatsapp_from,
        clients_sheet_url,
        resend_api_key,  # nova chave para envio de email via Resend API
    ):

        # Diretório onde os PDFs gerados serão armazenados
        self.report_output_dir = report_output_dir

        # Configurações SMTP (mantidas por compatibilidade / fallback)
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass

        # Configuração de remetente de email
        self.email_from_name = email_from_name
        self.email_from = email_from

        # Credenciais da API do Twilio (WhatsApp)
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token
        self.twilio_whatsapp_from = twilio_whatsapp_from

        # URL pública do Google Sheets contendo os clientes
        self.clients_sheet_url = clients_sheet_url

        # Chave da API Resend para envio de email via HTTP API
        self.resend_api_key = resend_api_key


    # ---------------------------------------------------------------------
    # Método estático responsável por carregar as configurações do .env
    # ou das variáveis definidas na cloud (Railway).
    # ---------------------------------------------------------------------
    @staticmethod
    def load() -> "Settings":

        # Carrega o arquivo .env local (em produção o Railway ignora isso)
        load_dotenv()

        return Settings(

            # Diretório onde os relatórios serão salvos
            report_output_dir=os.getenv("REPORT_OUTPUT_DIR", "./out"),

            # Configurações SMTP (podem ser removidas no futuro)
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER", ""),
            smtp_pass=os.getenv("SMTP_PASS", ""),

            # Configurações do remetente de email
            email_from_name=os.getenv("EMAIL_FROM_NAME", "Relatórios"),
            email_from=os.getenv("EMAIL_FROM", ""),

            # Credenciais Twilio para envio de WhatsApp
            twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
            twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
            twilio_whatsapp_from=os.getenv(
                "TWILIO_WHATSAPP_FROM",
                "whatsapp:+14155238886",
            ),

            # URL pública do Google Sheets que contém os clientes
            clients_sheet_url=os.getenv("CLIENTS_SHEET_URL"),

            # Chave da API Resend (usada para enviar email sem SMTP)
            resend_api_key=os.getenv("RESEND_API_KEY"),
        )