"""
config.py

Responsável por centralizar todas as configurações do sistema.

As configurações são carregadas do:
- arquivo .env (ambiente local)
- variáveis de ambiente da cloud (Railway)

A ideia é evitar espalhar os.getenv() pelo projeto inteiro.
"""

from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class Settings:
    """
    Classe que contém todas as configurações do sistema.
    """

    def __init__(
        self,

        # diretório de saída de relatórios
        report_output_dir,

        # configurações SMTP (mantido por compatibilidade)
        smtp_host,
        smtp_port,
        smtp_user,
        smtp_pass,

        # configuração de email remetente
        email_from_name,
        email_from,

        # Twilio WhatsApp
        twilio_account_sid,
        twilio_auth_token,
        twilio_whatsapp_from,

        # Google Sheets
        clients_sheet_url,

        # API Resend
        resend_api_key,

        # Google Ads API
        google_ads_developer_token,
        google_ads_client_id,
        google_ads_client_secret,
        google_ads_refresh_token,
        google_ads_login_customer_id,

        # flag para usar dados mockados (desenvolvimento e testes)  
        use_mock_data,
    ):

        # -----------------------------------------
        # diretório onde relatórios seriam gerados
        # -----------------------------------------
        self.report_output_dir = report_output_dir

        # -----------------------------------------
        # configurações SMTP (fallback antigo)
        # -----------------------------------------
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass

        # -----------------------------------------
        # configuração de remetente de email
        # -----------------------------------------
        self.email_from_name = email_from_name
        self.email_from = email_from

        # -----------------------------------------
        # credenciais Twilio (WhatsApp)
        # -----------------------------------------
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token
        self.twilio_whatsapp_from = twilio_whatsapp_from

        # -----------------------------------------
        # Google Sheets (lista de clientes)
        # -----------------------------------------
        self.clients_sheet_url = clients_sheet_url

        # -----------------------------------------
        # API Resend (envio de email via API)
        # -----------------------------------------
        self.resend_api_key = resend_api_key

        # -----------------------------------------
        # Google Ads API (MCC)
        # -----------------------------------------
        self.google_ads_developer_token = google_ads_developer_token
        self.google_ads_client_id = google_ads_client_id
        self.google_ads_client_secret = google_ads_client_secret
        self.google_ads_refresh_token = google_ads_refresh_token
        self.google_ads_login_customer_id = google_ads_login_customer_id
        
        # -----------------------------------------
        # flag para usar dados mockados (desenvolvimento e testes)
        # -----------------------------------------
        self.use_mock_data = use_mock_data

    @staticmethod
    def load() -> "Settings":
        """
        Carrega as configurações do sistema.

        1) primeiro tenta carregar o .env local
        2) se estiver rodando na cloud (Railway), usa variáveis do ambiente
        """

        # carrega .env local (em produção isso é ignorado)
        load_dotenv()

        return Settings(

            # -----------------------------------------
            # diretório de saída
            # -----------------------------------------
            report_output_dir=os.getenv("REPORT_OUTPUT_DIR", "./out"),

            # -----------------------------------------
            # SMTP
            # -----------------------------------------
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER", ""),
            smtp_pass=os.getenv("SMTP_PASS", ""),

            # -----------------------------------------
            # email remetente
            # -----------------------------------------
            email_from_name=os.getenv("EMAIL_FROM_NAME", "Relatórios"),
            email_from=os.getenv("EMAIL_FROM", ""),

            # -----------------------------------------
            # Twilio
            # -----------------------------------------
            twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
            twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
            twilio_whatsapp_from=os.getenv(
                "TWILIO_WHATSAPP_FROM",
                "whatsapp:+14155238886",
            ),

            # -----------------------------------------
            # Google Sheets
            # -----------------------------------------
            clients_sheet_url=os.getenv("CLIENTS_SHEET_URL"),

            # -----------------------------------------
            # Resend API
            # -----------------------------------------
            resend_api_key=os.getenv("RESEND_API_KEY"),

            # -----------------------------------------
            # Google Ads API
            # -----------------------------------------
            google_ads_developer_token=os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
            google_ads_client_id=os.getenv("GOOGLE_ADS_CLIENT_ID"),
            google_ads_client_secret=os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
            google_ads_refresh_token=os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
            google_ads_login_customer_id=os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),

            #   -----------------------------------------
            # flag para usar dados mockados (desenvolvimento e testes)
            #   -----------------------------------------
            use_mock_data=os.getenv("USE_MOCK_DATA", "true").lower() == "true",

        )