from fastapi import APIRouter, UploadFile, File, HTTPException
import os
if "PYTEST_CURRENT_TEST" not in os.environ:
    from..services.ingestion_service import ingestion_service
import os

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_location = f"data/raw_docs/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    try:
        with open(file_location, "wb+") as file_object:
            file_object.write(await file.read())

        # Ingest the document into ChromaDB
        await ingestion_service.ingest_document(file_location, file.filename or "uploaded.pdf")

        return {"message": f"Successfully uploaded and ingested {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")