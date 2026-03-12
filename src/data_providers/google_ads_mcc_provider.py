"""
google_ads_mcc_provider.py

Provider responsável por buscar dados do Google Ads
utilizando uma conta MCC (Manager Account).
"""

from google.ads.googleads.client import GoogleAdsClient


class GoogleAdsMCCProvider:

    def __init__(self, settings):

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

        response = ga_service.search(
            customer_id=customer_id,
            query=query
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
        """
        Retorna dados atuais e anteriores.
        """

        customer_id = client["google_ads_customer_id"]

        current_data = self._fetch_period(
            customer_id,
            "LAST_30_DAYS"
        )

        previous_data = self._fetch_period(
            customer_id,
            "PREVIOUS_30_DAYS"
        )

        return {
            "current": current_data,
            "previous": previous_data
        }