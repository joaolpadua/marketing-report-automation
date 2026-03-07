from dataclasses import dataclass
from dotenv import load_dotenv
import os


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
    ):
        self.report_output_dir = report_output_dir
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.email_from_name = email_from_name
        self.email_from = email_from
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token
        self.twilio_whatsapp_from = twilio_whatsapp_from
        self.clients_sheet_url = clients_sheet_url

    @staticmethod
    def load() -> "Settings":
        load_dotenv()

        return Settings(
            report_output_dir=os.getenv("REPORT_OUTPUT_DIR", "./out"),
            smtp_host=os.getenv("SMTP_HOST", ""),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_user=os.getenv("SMTP_USER", ""),
            smtp_pass=os.getenv("SMTP_PASS", ""),
            email_from_name=os.getenv("EMAIL_FROM_NAME", "Relatórios"),
            email_from=os.getenv("EMAIL_FROM", ""),
            twilio_account_sid=os.getenv("TWILIO_ACCOUNT_SID", ""),
            twilio_auth_token=os.getenv("TWILIO_AUTH_TOKEN", ""),
            twilio_whatsapp_from=os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886"),
            clients_sheet_url=os.getenv("CLIENTS_SHEET_URL"),
        )