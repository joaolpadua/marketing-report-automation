"""
comparison.py

Responsável por comparar métricas entre dois períodos
e calcular a variação percentual.
"""


def calculate_change(current, previous):
    """
    Calcula variação percentual entre dois valores.
    """

    if previous == 0:
        return 0

    change = ((current - previous) / previous) * 100
    return round(change, 2)


def compare_metrics(current_metrics, previous_metrics):
    """
    Recebe métricas atuais e anteriores e retorna variações.
    """

    return {
        "clicks_change": calculate_change(
            current_metrics["clicks"], previous_metrics["clicks"]
        ),
        "impressions_change": calculate_change(
            current_metrics["impressions"], previous_metrics["impressions"]
        ),
        "conversions_change": calculate_change(
            current_metrics["conversions"], previous_metrics["conversions"]
        ),
        "cpa_change": calculate_change(
            current_metrics["cpa_brl"], previous_metrics["cpa_brl"]
        ),
    }