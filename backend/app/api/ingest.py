from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from pydantic import BaseModel
from typing import Optional
import os
if "PYTEST_CURRENT_TEST" not in os.environ:
    from ..services.ingestion_service import ingestion_service

router = APIRouter()

SUPPORTED_EXTENSIONS = [".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"]

class LinkIngestRequest(BaseModel):
    link: str

@router.post("/upload")
async def upload_document(
    file: Optional[UploadFile] = File(None),
    link_req: Optional[LinkIngestRequest] = Body(None)
):
    if file:
        filename = file.filename or "uploaded_file"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

        upload_dir = "/app/data/raw_docs"
        os.makedirs(upload_dir, exist_ok=True)
        file_location = os.path.join(upload_dir, filename)

        try:
            with open(file_location, "wb+") as file_object:
                file_object.write(await file.read())

            await ingestion_service.ingest_document(file_location, filename)
            return {"message": f"Successfully uploaded and ingested {filename}"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
    elif link_req and link_req.link:
        try:
            await ingestion_service.ingest_link(str(link_req.link))
            return {"message": f"Successfully ingested link: {link_req.link}"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process link: {e}")
    else:
        raise HTTPException(status_code=400, detail="No file or link provided.")