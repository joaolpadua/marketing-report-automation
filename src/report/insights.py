"""
insights.py

Responsável por transformar métricas em comentários interpretáveis
para o cliente.

A ideia é simular o feedback que um analista de marketing faria
ao olhar os números da campanha.
"""


def generate_insights(metrics, comparison):
    """
    Gera uma lista de insights automáticos baseados nas métricas.

    Retorna:
        list[str]
    """

    insights = []

    # -----------------------------
    # CTR
    # -----------------------------

    if metrics["ctr"] < 3:
        insights.append(
            "CTR está baixo. Pode ser interessante revisar criativos ou segmentação."
        )

    if comparison["ctr_change"] > 10:
        insights.append(
            "CTR melhorou em relação ao período anterior."
        )

    if comparison["ctr_change"] < -10:
        insights.append(
            "CTR caiu em relação ao período anterior."
        )

    # -----------------------------
    # Conversões
    # -----------------------------

    if comparison["conversions_change"] > 10:
        insights.append(
            "Conversões aumentaram em relação ao período anterior."
        )

    if comparison["conversions_change"] < -10:
        insights.append(
            "Conversões diminuíram em relação ao período anterior."
        )

    # -----------------------------
    # CPA
    # -----------------------------

    if metrics["cpa_brl"] < 20:
        insights.append(
            "Custo por aquisição está eficiente."
        )

    if metrics["cpa_brl"] > 50:
        insights.append(
            "CPA está alto. Pode ser interessante revisar a estratégia de conversão."
        )

    return insights