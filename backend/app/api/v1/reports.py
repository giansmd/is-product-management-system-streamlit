from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
import io
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/inventory/pdf")
def download_inventory_pdf(
    categoria: str | None = Query(None),
    db: Session = Depends(get_db),
):
    service = ReportService(db)
    pdf_bytes = service.generate_inventory_pdf(categoria=categoria)
    filename = f"inventario{'_' + categoria if categoria else ''}.pdf"
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
