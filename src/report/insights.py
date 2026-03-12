"""
insights.py

Gera interpretações automáticas das métricas.
"""


def generate_insights(metrics):

    insights = []

    if metrics["ctr"] > 5:
        insights.append("CTR está alto, indicando bom engajamento dos anúncios.")
    else:
        insights.append("CTR está baixo. Pode ser interessante revisar criativos ou segmentação.")

    if metrics["cpa_brl"] < 20:
        insights.append("Custo por aquisição está eficiente.")
    else:
        insights.append("Custo por aquisição está elevado.")

    return insights