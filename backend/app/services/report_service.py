import io
from decimal import Decimal

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.repository.product_repository import ProductRepository
from sqlalchemy.orm import Session


class ReportService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def generate_inventory_pdf(self, categoria: str | None = None) -> bytes:
        items, _ = self.repo.get_all(limit=10000, categoria=categoria)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm)
        styles = getSampleStyleSheet()
        elements = []

        title = Paragraph("Reporte de Inventario de Productos", styles["Title"])
        elements.append(title)
        if categoria:
            elements.append(Paragraph(f"Categoría: {categoria}", styles["Normal"]))
        elements.append(Spacer(1, 0.5 * cm))

        header = ["SKU", "Nombre", "Categoría", "Stock Actual", "Precio Venta", "Valor"]
        table_data = [header]
        for p in items:
            valor = Decimal(str(p.precio_venta)) * p.stock_actual
            table_data.append([
                p.sku,
                p.nombre[:40],
                p.categoria,
                str(p.stock_actual),
                f"${p.precio_venta:,.2f}",
                f"${valor:,.2f}",
            ])

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2563EB")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#EFF6FF")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 1), (-1, -1), 9),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(table)

        doc.build(elements)
        buffer.seek(0)
        return buffer.read()
