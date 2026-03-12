"""
comparison.py

Responsável por comparar métricas entre dois períodos
(ex: semana atual vs semana anterior).
"""


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