
# RAGChatbot Docker & Deployment Guide

---

## Quick Start

1. **Build and run all services:**
   ```sh
   docker compose up --build
   ```

2. **Service URLs:**
   - FastAPI backend (rag-api): [http://localhost:8001](http://localhost:8001)
   - ChromaDB vector database: [http://localhost:8000](http://localhost:8000)
   - Ollama LLM API: [http://localhost:11434](http://localhost:11434)
   - Chatbot UI: [http://localhost:3000](http://localhost:3000)

---

## Expose Your Project Publicly with Ngrok

You can use [Ngrok](https://ngrok.com/) to share your local services for quick demos or remote access.

**Expose the FastAPI backend:**
1. [Download Ngrok](https://ngrok.com/download) and install it.
2. Start your stack as above.
3. In a new terminal, run:
   ```sh
   ngrok http 8001
   ```
   Ngrok will provide a public URL forwarding to your FastAPI backend.

**Expose other ports:**
   - For the UI: `ngrok http 3000`
   - For ChromaDB: `ngrok http 8000`

**Security note:** For production or sensitive data, always use authentication and HTTPS with Ngrok.

---

## Deploying to the Cloud

1. **Build your image:**
   ```sh
   docker build -t myapp .
   ```
2. **For different CPU architectures:**
   ```sh
   docker build --platform=linux/amd64 -t myapp .
   ```
3. **Push to your registry:**
   ```sh
   docker push myregistry.com/myapp
   ```
4. See Docker's [getting started guide](https://docs.docker.com/go/get-started-sharing/) for more details.

---

## References
- [Docker's Python guide](https://docs.docker.com/language/python/)