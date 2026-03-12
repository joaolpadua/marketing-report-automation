"""
validation.py

Validação básica de dados de cliente antes de processar o pipeline.
"""


def validate_client(client):
    """
    Verifica se o cliente possui os campos obrigatórios.
    """

    if not client.get("client_name"):
        raise ValueError("Cliente sem 'client_name'")

    if not client.get("whatsapp_e164"):
        raise ValueError("Cliente sem 'whatsapp_e164'")