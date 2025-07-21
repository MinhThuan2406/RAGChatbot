from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, Any
import os
import aiofiles
from pathlib import Path
from app.services.ingestion_service import IngestionService

router = APIRouter()
ingestion_service = IngestionService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload and ingest a document.
    Supports PDF, DOCX, TXT, and image files.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    # Create upload directory
    upload_dir = Path("/app/data/raw_docs")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_location = upload_dir / file.filename

    try:
        # Save uploaded file
        async with aiofiles.open(file_location, "wb") as file_object:
            content = await file.read()
            await file_object.write(content)

        # Ingest the document
        result = await ingestion_service.ingest_document(str(file_location), file.filename)
        
        # Return appropriate HTTP status based on ingestion result
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        elif result["status"] == "warning":
            return {
                "message": result["message"],
                "warning": True,
                "file_name": result["file_name"]
            }
        else:
            return {
                "message": result["message"],
                "file_name": result["file_name"],
                "chunks_created": result.get("chunks_created", 0),
                "document_type": result.get("document_type", "unknown"),
                "embedding_provider": result.get("embedding_provider", "unknown")
            }
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Clean up file if ingestion failed
        if file_location.exists():
            try:
                file_location.unlink()
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/upload-directory")
async def ingest_directory(directory_path: str) -> Dict[str, Any]:
    """
    Ingest all supported documents from a specified directory.
    """
    if not directory_path:
        raise HTTPException(status_code=400, detail="Directory path is required.")
    
    try:
        result = await ingestion_service.ingest_directory(directory_path)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=500, detail=result["message"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process directory: {str(e)}")

@router.get("/supported-types")
async def get_supported_types() -> Dict[str, Any]:
    """
    Get list of supported document types.
    """
    return {
        "supported_extensions": [".pdf", ".docx", ".txt", ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif"],
        "document_types": {
            "PDF": "Portable Document Format files",
            "DOCX": "Microsoft Word documents (newer format)",
            "TXT": "Plain text files",
            "Images": "Image files with OCR text extraction (requires Tesseract)"
        },
        "note": "DOC files are not currently supported but can be converted to DOCX",
        "ocr_availability": "Available" if _check_tesseract_availability() else "Not available - install Tesseract for image processing"
    }

def _check_tesseract_availability() -> bool:
    """Check if Tesseract OCR is available"""
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True
    except:
        return False
