"""
data_sources.py

Combina todas as fontes de dados do sistema:
- Clientes do Google Sheets
- Google Ads API (MCC Provider)
- Mock Provider para testes
"""

import pandas as pd
import requests
import random
from io import StringIO
from google.ads.googleads.client import GoogleAdsClient


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

    clients = df.to_dict(orient="records")
    
    # normaliza telefones
    for client in clients:
        raw_phone = str(client.get("whatsapp_e164", "")).strip()
        if raw_phone and not raw_phone.startswith("+"):
            raw_phone = "+" + raw_phone
        client["whatsapp_e164"] = raw_phone

    return clients


class GoogleAdsMCCProvider:
    """Provider responsável por buscar dados do Google Ads usando conta MCC."""

    def __init__(self, settings):
        """Inicializa cliente da Google Ads API."""
        print("Google Ads MCC Provider carregado")

        config = {
            "developer_token": settings.google_ads_developer_token,
            "client_id": settings.google_ads_client_id,
            "client_secret": settings.google_ads_client_secret,
            "refresh_token": settings.google_ads_refresh_token,
            "login_customer_id": settings.google_ads_login_customer_id,
            "use_proto_plus": True
        }

        self.client = GoogleAdsClient.load_from_dict(config)

    def _fetch_period(self, customer_id, period):
        """Executa query na API do Google Ads para um período específico."""
        print(f"Buscando dados Google Ads para {customer_id} | período {period}")

        query = f"""
        SELECT
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions
        FROM campaign
        WHERE segments.date DURING {period}
        """

        ga_service = self.client.get_service("GoogleAdsService")

        try:
            response = ga_service.search(
                customer_id=customer_id,
                query=query
            )
        except Exception as exc:
            raise RuntimeError(
                f"Erro ao consultar Google Ads para {customer_id}: {exc}"
            )

        results = []
        for row in response:
            results.append({
                "campaign_name": row.campaign.name,
                "impressions": row.metrics.impressions,
                "clicks": row.metrics.clicks,
                "cost": row.metrics.cost_micros / 1_000_000,
                "conversions": row.metrics.conversions
            })

        return results

    def get_campaign_data(self, client):
        """Retorna dados de dois períodos: últimos 30 dias e 30 dias anteriores."""
        customer_id = client.get("google_ads_customer_id")

        if not customer_id:
            raise ValueError(
                f"Cliente {client['client_name']} não possui google_ads_customer_id"
            )

        customer_id = customer_id.replace("-", "")

        current_data = self._fetch_period(customer_id, "LAST_30_DAYS")
        previous_data = self._fetch_period(customer_id, "PREVIOUS_30_DAYS")

        return {
            "current": current_data,
            "previous": previous_data
        }


class MockProvider:
    """Provider para testes com dados simulados."""

    def generate_campaigns(self):
        """Gera campanhas simuladas para um período."""
        campaigns = ["Search Brand", "Search Produto", "Display Remarketing"]
        results = []

        for campaign in campaigns:
            impressions = random.randint(5000, 20000)
            clicks = random.randint(100, 800)
            cost = round(random.uniform(100, 800), 2)
            conversions = random.randint(5, 40)

            results.append({
                "campaign_name": campaign,
                "impressions": impressions,
                "clicks": clicks,
                "cost": cost,
                "conversions": conversions
            })

        return results

    def get_campaign_data(self, client):
        """Retorna dados simulados para dois períodos."""
        current_data = self.generate_campaigns()
        previous_data = self.generate_campaigns()

        return {
            "current": current_data,
            "previous": previous_data
        }
