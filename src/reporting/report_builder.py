def build_report(client, metrics, comparison, insights):

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