"""
delivery.py

Combina toda a lógica de entrega:
- Envio de WhatsApp via Twilio
- Armazenamento local de relatórios
"""

import requests
import datetime
from pathlib import Path


def send_whatsapp_message_with_media(
    account_sid: str,
    auth_token: str,
    from_whatsapp: str,
    to_whatsapp: str,
    message: str,
    media_url: str | None = None,
) -> None:
    """
    Envia uma mensagem de WhatsApp utilizando a API do Twilio.
    """
    # Validação básica de credenciais
    if not account_sid or not auth_token:
        raise RuntimeError("Credenciais do Twilio não configuradas.")

    # Normaliza telefone
    to_whatsapp = str(to_whatsapp)
    to_whatsapp = to_whatsapp.replace("whatsapp:", "").replace("+", "")
    to_whatsapp = f"whatsapp:+{to_whatsapp}"

    # Endpoint da API Twilio
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    # Corpo da requisição HTTP
    data = {
        "From": from_whatsapp,
        "To": to_whatsapp,
        "Body": message,
    }

    # Se existir mídia adiciona no payload
    if media_url:
        data["MediaUrl"] = media_url

    # Requisição POST para API Twilio
    response = requests.post(
        url,
        data=data,
        auth=(account_sid, auth_token),
        timeout=30,
    )

    # Verificação de erro na API
    if response.status_code >= 300:
        raise RuntimeError(
            f"Erro Twilio {response.status_code}: {response.text}"
        )


def save_report(run_id: str, client_name: str, message: str):
    """
    Salva o relatório localmente para histórico.
    """
    base_path = Path("reports") / run_id
    base_path.mkdir(parents=True, exist_ok=True)

    filename = client_name.lower().replace(" ", "_") + ".txt"
    filepath = base_path / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(message)

    return filepath
