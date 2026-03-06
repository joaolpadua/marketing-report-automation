import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def build_pdf_report(client: dict, metrics: dict, output_dir: str) -> str:
    """
    Gera um relatório PDF simples com métricas do cliente.
    """
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"relatorio_{client['client_id']}_{metrics['period_label'].replace('/', '-')}.pdf"
    pdf_path = os.path.join(output_dir, file_name)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 60, "Relatório de Marketing")

    c.setFont("Helvetica", 11)
    c.drawString(40, height - 90, f"Cliente: {client['client_name']}")
    c.drawString(40, height - 110, f"Período: {metrics['period_label']}")
    c.drawString(40, height - 130, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 170, "Resumo de Performance")

    c.setFont("Helvetica", 11)
    lines = [
        f"Cliques: {metrics['clicks']}",
        f"Impressões: {metrics['impressions']}",
        f"CTR: {metrics['ctr']}%",
        f"Custo: R$ {metrics['cost_brl']:.2f}",
        f"Conversões: {metrics['conversions']}",
        f"CPA: R$ {metrics['cpa_brl']:.2f}",
    ]

    y = height - 200
    for line in lines:
        c.drawString(60, y, f"- {line}")
        y -= 20

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(40, 40, "Relatório gerado automaticamente por script Python.")

    c.save()
    return pdf_path