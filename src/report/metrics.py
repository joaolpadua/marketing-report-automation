"""
metrics.py

Responsável por calcular métricas agregadas de campanhas.
Mantém toda a lógica matemática do sistema isolada.
"""


def aggregate_metrics(campaign_data):
    """
    Recebe lista de campanhas e retorna métricas consolidadas.
    """

    impressions = sum(c["impressions"] for c in campaign_data)
    clicks = sum(c["clicks"] for c in campaign_data)
    cost = sum(c["cost"] for c in campaign_data)
    conversions = sum(c["conversions"] for c in campaign_data)

    ctr = (clicks / impressions * 100) if impressions else 0
    cpc = (cost / clicks) if clicks else 0
    cpa = (cost / conversions) if conversions else 0

    return {
        "period_label": "Últimos 30 dias",
        "impressions": impressions,
        "clicks": clicks,
        "cost_brl": round(cost, 2),
        "conversions": conversions,
        "ctr": round(ctr, 2),
        "cpc": round(cpc, 2),
        "cpa_brl": round(cpa, 2),
    }