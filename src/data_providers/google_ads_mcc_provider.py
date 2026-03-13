"""
google_ads_mcc_provider.py

Provider responsável por buscar dados do Google Ads
utilizando uma conta MCC (Manager Account).

Esse provider permite que uma agência consulte
múltiplas contas de clientes através de uma conta
gerenciadora (MCC).

Fluxo geral:

run.py
 ↓
GoogleAdsMCCProvider
 ↓
Google Ads API
 ↓
dados de campanhas
 ↓
pipeline de métricas do sistema
"""

from google.ads.googleads.client import GoogleAdsClient


class GoogleAdsMCCProvider:

    def __init__(self, settings):
        """
        Inicializa cliente da Google Ads API.

        As credenciais são carregadas do Settings
        que por sua vez lê variáveis de ambiente.
        """

        print("Google Ads MCC Provider carregado")

        config = {
            "developer_token": settings.google_ads_developer_token,
            "client_id": settings.google_ads_client_id,
            "client_secret": settings.google_ads_client_secret,
            "refresh_token": settings.google_ads_refresh_token,
            "login_customer_id": settings.google_ads_login_customer_id,
            "use_proto_plus": True
        }

        # cria cliente da API
        self.client = GoogleAdsClient.load_from_dict(config)


    def _fetch_period(self, customer_id, period):
        """
        Executa query na API do Google Ads para um período específico.

        Args:
            customer_id (str): ID da conta Google Ads
            period (str): intervalo de datas (ex: LAST_30_DAYS)

        Returns:
            list[dict]: lista de campanhas com métricas básicas
        """

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

                # custo vem em micros → converter para moeda real
                "cost": row.metrics.cost_micros / 1_000_000,

                "conversions": row.metrics.conversions
            })

        return results


    def get_campaign_data(self, client):
        """
        Método principal chamado pelo pipeline.

        Retorna dados de dois períodos:
        - últimos 30 dias
        - 30 dias anteriores

        Estrutura de retorno:

        {
            "current": [...],
            "previous": [...]
        }
        """

        customer_id = client.get("google_ads_customer_id")

        # valida se cliente possui id de conta
        if not customer_id:
            raise ValueError(
                f"Cliente {client['client_name']} não possui google_ads_customer_id"
            )

        # remover traços (Google Ads API exige sem traços)
        customer_id = customer_id.replace("-", "")

        # buscar dados atuais
        current_data = self._fetch_period(
            customer_id,
            "LAST_30_DAYS"
        )

        # buscar dados período anterior
        previous_data = self._fetch_period(
            customer_id,
            "PREVIOUS_30_DAYS"
        )

        return {
            "current": current_data,
            "previous": previous_data
        }