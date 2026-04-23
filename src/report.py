"""
report.py

Combina toda a lógica de geração de relatórios:
- Cálculo de métricas agregadas
- Comparação entre períodos
- Geração de insights automáticos
- Montagem da mensagem final
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


def percentage_change(current, previous):
    """
    Calcula variação percentual entre dois valores.
    Protege contra divisão por zero.
    """
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100, 2)


def compare_metrics(current, previous):
    """
    Compara dois conjuntos de métricas e retorna as variações.
    """
    return {
        "clicks_change": percentage_change(
            current["clicks"],
            previous["clicks"]
        ),
        "impressions_change": percentage_change(
            current["impressions"],
            previous["impressions"]
        ),
        "conversions_change": percentage_change(
            current["conversions"],
            previous["conversions"]
        ),
        "ctr_change": percentage_change(
            current["ctr"],
            previous["ctr"]
        ),
        "cpa_change": percentage_change(
            current["cpa_brl"],
            previous["cpa_brl"]
        )
    }


def generate_insights(metrics, comparison):
    """
    Gera uma lista de insights automáticos baseados nas métricas.
    Simula o feedback que um analista de marketing faria.
    """
    insights = []

    # CTR
    if metrics["ctr"] < 3:
        insights.append(
            "CTR está baixo. Pode ser interessante revisar criativos ou segmentação."
        )

    if comparison["ctr_change"] > 10:
        insights.append("CTR melhorou em relação ao período anterior.")

    if comparison["ctr_change"] < -10:
        insights.append("CTR caiu em relação ao período anterior.")

    # Conversões
    if comparison["conversions_change"] > 10:
        insights.append("Conversões aumentaram em relação ao período anterior.")

    if comparison["conversions_change"] < -10:
        insights.append("Conversões diminuíram em relação ao período anterior.")

    # CPA
    if metrics["cpa_brl"] < 20:
        insights.append("CPA está eficiente, indicando bom custo por aquisição.")

    if comparison["cpa_change"] < -10:
        insights.append("CPA melhorou em relação ao período anterior.")

    if comparison["cpa_change"] > 10:
        insights.append("CPA piorou em relação ao período anterior.")

    return insights


def build_report(client, metrics, comparison, insights):
    """
    Monta a mensagem final do relatório para envio via WhatsApp.
    """
    message = (
        f"📊 Relatório de Marketing\n\n"
        f"Cliente: {client['client_name']}\n"
        f"Período: Últimos 30 dias\n\n"

        f"Cliques: {metrics['clicks']} ({comparison['clicks_change']}%)\n"
        f"Impressões: {metrics['impressions']} ({comparison['impressions_change']}%)\n"
        f"CTR: {metrics['ctr']}%\n"
        f"Custo: R$ {metrics['cost_brl']}\n"
        f"Conversões: {metrics['conversions']} ({comparison['conversions_change']}%)\n"
        f"CPA: R$ {metrics['cpa_brl']} ({comparison['cpa_change']}%)\n"
    )

    if insights:
        message += "\n💡 Insights\n"
        for insight in insights:
            message += f"* {insight}\n"

    return message
