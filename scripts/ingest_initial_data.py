# scripts/ingest_initial_data.py
import httpx
import asyncio
import os

# Assuming your FastAPI backend is accessible at http://localhost:8001
FASTAPI_URL = "http://localhost:8001"
INGEST_ENDPOINT = f"{FASTAPI_URL}/api/ingest/upload"
DATA_DIR = "./data/raw_docs"

async def ingest_all_documents():
    print(f"Starting ingestion of documents from {DATA_DIR}...")
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(file_path):
            print(f"Ingesting {filename}...")
            try:
                async with httpx.AsyncClient() as client:
                    with open(file_path, "rb") as f:
                        files = {"file": (filename, f, "application/pdf")} # Adjust content type if not PDF
                        response = await client.post(INGEST_ENDPOINT, files=files, timeout=300)
                        response.raise_for_status()
                        print(f"Successfully ingested {filename}: {response.json()}")
            except httpx.HTTPStatusError as e:
                print(f"Failed to ingest {filename}: HTTP error {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                print(f"Failed to ingest {filename}: Request error - {e}")
            except Exception as e:
                print(f"An unexpected error occurred during ingestion of {filename}: {e}")
    print("Ingestion process completed.")

if __name__ == "__main__":
    asyncio.run(ingest_all_documents())