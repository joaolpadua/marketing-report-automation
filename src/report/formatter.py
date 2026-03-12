"""
formatter.py

Responsável por montar o relatório final que será enviado ao cliente.
"""


def build_whatsapp_report(client, metrics, insights):

    insights_text = "\n".join([f"• {i}" for i in insights])

    return (
        f"📊 Relatório de Marketing\n\n"
        f"Cliente: {client['client_name']}\n"
        f"Período: {metrics['period_label']}\n\n"
        f"Cliques: {metrics['clicks']}\n"
        f"Impressões: {metrics['impressions']}\n"
        f"CTR: {metrics['ctr']}%\n"
        f"Custo: R$ {metrics['cost_brl']}\n"
        f"Conversões: {metrics['conversions']}\n"
        f"CPA: R$ {metrics['cpa_brl']}\n\n"
        f"💡 Insights\n"
        f"{insights_text}"
    )