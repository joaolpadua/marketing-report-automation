from dataclasses import dataclass
from dotenv import load_dotenv
import os


@dataclass
class Settings:
    report_output_dir: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    email_from_name: str
    email_from: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_whatsapp_from: str

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
        )