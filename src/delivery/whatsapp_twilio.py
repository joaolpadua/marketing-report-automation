import requests


def send_whatsapp_message_with_media(
    account_sid: str,
    auth_token: str,
    from_whatsapp: str,
    to_whatsapp: str,
    message: str,
    media_url: str | None = None,
) -> None:
    """
    Envia uma mensagem por WhatsApp usando Twilio.
    Neste primeiro momento, vamos deixar pronto mas não obrigar o uso.
    """

    if not account_sid or not auth_token:
        raise RuntimeError("Credenciais do Twilio não configuradas.")

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    data = {
        "From": from_whatsapp,
        "To": f"whatsapp:{to_whatsapp}",
        "Body": message,
    }

    if media_url:
        data["MediaUrl"] = media_url

    response = requests.post(
        url,
        data=data,
        auth=(account_sid, auth_token),
        timeout=30,
    )

    if response.status_code >= 300:
        raise RuntimeError(f"Erro Twilio {response.status_code}: {response.text}")