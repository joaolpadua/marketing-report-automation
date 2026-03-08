import requests


def send_email_with_attachment(
    api_key: str,
    from_email: str,
    to_email: str,
    subject: str,
    body: str,
):
    """
    Envia email usando Resend API.
    Não usa SMTP, funciona melhor em cloud.
    """

    url = "https://api.resend.com/emails"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "from": from_email,
        "to": [to_email],
        "subject": subject,
        "html": f"<p>{body}</p>",
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code >= 300:
        raise RuntimeError(f"Erro envio email: {response.text}")