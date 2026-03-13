from src.data_providers.mock_provider import MockProvider
from src.report.metrics import aggregate_metrics
from src.report.comparison import compare_metrics
from src.report.insights import generate_insights


def test_full_pipeline_runs_successfully():

    provider = MockProvider()

    # mock_provider retorna current e previous
    data = provider.get_campaign_data(client={})

    current_data = data["current"]
    previous_data = data["previous"]

    # cálculo de métricas
    metrics_current = aggregate_metrics(current_data)
    metrics_previous = aggregate_metrics(previous_data)

    # comparação
    comparison = compare_metrics(metrics_current, metrics_previous)

    # geração de insights
    insights = generate_insights(metrics_current, comparison)

    assert isinstance(metrics_current, dict)
    assert isinstance(comparison, dict)
    assert isinstance(insights, list)