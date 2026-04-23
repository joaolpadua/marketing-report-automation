"""
utils.py

Funções utilitárias do sistema.
"""

import datetime


def generate_run_id():
    """Gera ID único para execução do job."""
    now = datetime.datetime.utcnow()
    return now.strftime("run_%Y_%m_%d_%H%M")


def validate_client(client):
    """Verifica se o cliente possui os campos obrigatórios."""
    if not client.get("client_name"):
        raise ValueError("Cliente sem 'client_name'")
    if not client.get("whatsapp_e164"):
        raise ValueError("Cliente sem 'whatsapp_e164'")
