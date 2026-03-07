import pandas as pd
import requests
from io import StringIO


def load_clients_from_sheets(csv_url: str):
    """
    Carrega clientes a partir de uma planilha Google Sheets publicada como CSV.
    Retorna uma lista de dicionários (mesmo formato usado no resto do sistema).
    """

    response = requests.get(csv_url)
    response.raise_for_status()

    csv_data = StringIO(response.text)

    df = pd.read_csv(csv_data)

    # filtra apenas clientes ativos
    if "active" in df.columns:
        df = df[df["active"].astype(str).str.lower() == "true"]

    return df.to_dict(orient="records")