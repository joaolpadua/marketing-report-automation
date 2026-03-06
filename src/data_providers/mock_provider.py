from datetime import date


class MockProvider:
    """
    Provider fake para simular dados de marketing.
    Serve para testar o fluxo completo sem depender da API do Google ainda.
    """

    def get_monthly_metrics(self, client: dict) -> dict:
        today = date.today()
        period_label = f"{today.month:02d}/{today.year}"

        clicks = 1200
        impressions = 50000
        ctr = round((clicks / impressions) * 100, 2)
        cost_brl = 850.00
        conversions = 34
        cpa_brl = round(cost_brl / max(conversions, 1), 2)

        return {
            "period_label": period_label,
            "clicks": clicks,
            "impressions": impressions,
            "ctr": ctr,
            "cost_brl": cost_brl,
            "conversions": conversions,
            "cpa_brl": cpa_brl,
        }