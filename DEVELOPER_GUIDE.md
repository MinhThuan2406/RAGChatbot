# RAGChatbot Developer Guide

This guide is for developers who want to understand, extend, or contribute to the RAGChatbot project.

---

## 1. Project Structure

- `backend/` — FastAPI backend, adapters, core logic, database, and services
- `frontend/` — Web UI (if present)
- `data/raw_docs/` — Place for raw documents to be ingested
- `open-webui/` — Optional advanced web UI and related scripts
- `scripts/` — Utility scripts (e.g., data ingestion)

---

## 2. Setting Up for Development

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Node.js (for frontend development)

### Backend Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run backend locally:
   ```sh
   uvicorn backend.app.main:app --reload --port 8001
   ```

### Frontend Setup (if applicable)
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   npm install
   npm run dev
   ```

---

## 3. Running with Docker
- Use `docker compose up --build` to start all services.
- Edit `compose.yml` to add or modify services.

---

## 4. API Endpoints
- Main API: `/api/`
- Chat: `/api/chat`
- Ingest: `/api/ingest/upload`
- See `backend/app/api/` for more endpoints and details.

---

## 5. Testing
- Tests are in `backend/tests/`.
- Run tests with:
  ```sh
  pytest backend/tests/
  ```

---

## 6. Adding New Models or Adapters
- Add new adapters in `backend/app/adapters/`.
- Register them in the main app as needed.

---

## 7. Environment Variables
- Configure via `.env` in the project root.
- See `README.Docker.md` for variable descriptions.

---

## 8. Useful Scripts
- `scripts/ingest_initial_data.py` — Ingests all documents in `data/raw_docs/`.

---

## 9. Contributing
- See `open-webui/docs/CONTRIBUTING.md` for contribution guidelines.

---

## 10. Troubleshooting
- See `TROUBLESHOOTING.md` for common issues and solutions.
