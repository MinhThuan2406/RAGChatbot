import httpx
import asyncio
import os

FASTAPI_URL = "http://localhost:8001"
INGEST_ENDPOINT = f"{FASTAPI_URL}/api/ingest/upload"
DATA_DIR = "./data/raw_docs"

async def ingest_all_documents():
    success, fail = 0, 0
    print(f"Starting ingestion of documents from {DATA_DIR}...")
    for filename in os.listdir(DATA_DIR):
        if not filename.lower().endswith(".pdf"):
            print(f"Skipping non-PDF file: {filename}")
            continue
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(file_path):
            print(f"Ingesting {filename}...")
            try:
                async with httpx.AsyncClient() as client:
                    with open(file_path, "rb") as f:
                        files = {"file": (filename, f, "application/pdf")}
                        response = await client.post(INGEST_ENDPOINT, files=files, timeout=300)
                        response.raise_for_status()
                        print(f"Successfully ingested {filename}: {response.json()}")
                        success += 1
            except Exception as e:
                print(f"Failed to ingest {filename}: {e}")
                fail += 1
    print(f"Ingestion process completed. Success: {success}, Failed: {fail}")

if __name__ == "__main__":
    asyncio.run(ingest_all_documents())