import pandas as pd


def load_clients(path: str) -> list[dict]:
    """
    Lê o CSV de clientes e devolve uma lista de dicionários.
    Também normaliza o telefone para o formato esperado.
    """
    df = pd.read_csv(path, dtype=str).fillna("")
    clients = df.to_dict(orient="records")

    for client in clients:
        raw_phone = client.get("whatsapp_e164", "").strip()

        if raw_phone and not raw_phone.startswith("+"):
            raw_phone = "+" + raw_phone

        client["whatsapp_e164"] = raw_phone

    return clients