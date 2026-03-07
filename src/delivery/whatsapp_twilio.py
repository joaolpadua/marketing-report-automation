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
    Envia uma mensagem de WhatsApp utilizando a API do Twilio.

    Parâmetros
    ----------
    account_sid : str
        Identificador da conta Twilio.

    auth_token : str
        Token de autenticação da conta Twilio.

    from_whatsapp : str
        Número de origem configurado no Twilio Sandbox.
        Exemplo: "whatsapp:+14155238886"

    to_whatsapp : str
        Número do destinatário (somente números).
        Exemplo: "5516999133504"

    message : str
        Texto da mensagem que será enviada.

    media_url : str | None
        URL de mídia opcional (imagem, PDF, etc).
        No nosso caso inicial deixaremos None.
    """

    # ----------------------------
    # Validação básica de credenciais
    # ----------------------------
    if not account_sid or not auth_token:
        raise RuntimeError("Credenciais do Twilio não configuradas.")

    # ----------------------------
    # normaliza telefone
    to_whatsapp = str(to_whatsapp)
    to_whatsapp = to_whatsapp.replace("whatsapp:", "").replace("+", "")
    to_whatsapp = f"whatsapp:+{to_whatsapp}"

    # ----------------------------
    # Endpoint da API Twilio
    # ----------------------------
    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"

    # ----------------------------
    # Corpo da requisição HTTP
    # ----------------------------
    data = {
        "From": from_whatsapp,
        "To": to_whatsapp,
        "Body": message,
    }

    # ----------------------------
    # Se existir mídia adiciona no payload
    # ----------------------------
    if media_url:
        data["MediaUrl"] = media_url



    # ----------------------------
    # Requisição POST para API Twilio
    # ----------------------------
    response = requests.post(
        url,
        data=data,
        auth=(account_sid, auth_token),
        timeout=30,
    )

    # ----------------------------
    # Verificação de erro na API
    # ----------------------------
    if response.status_code >= 300:
        raise RuntimeError(
            f"Erro Twilio {response.status_code}: {response.text}"
        )