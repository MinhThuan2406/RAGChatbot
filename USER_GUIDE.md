# RAGChatbot User Guide

Welcome to RAGChatbot! This guide will help you get started as an end-user, from running the chatbot to interacting with its features.

---

## 1. What is RAGChatbot?
RAGChatbot is a modular, containerized chatbot system that uses Retrieval-Augmented Generation (RAG) to provide intelligent, context-aware responses. It leverages FastAPI, ChromaDB, Ollama, and a modern web UI.

---

## 2. Quick Start for Users

### Prerequisites
- Docker and Docker Compose installed
- (Optional) Ngrok for remote access

### Running the Chatbot
1. Open a terminal in the project root directory.
2. Start all services:
   ```sh
   docker compose up --build
   ```
3. Access the services:
   - **Chatbot UI:** [http://localhost:3000](http://localhost:3000)
   - **API:** [http://localhost:8001](http://localhost:8001)

### Using the Chatbot
- Open your browser and go to the Chatbot UI URL.
- Start chatting! The chatbot will use your uploaded documents and integrated LLMs to answer questions.

---

## 3. Uploading Documents
- Place your files in the `data/raw_docs/` directory.
- Use the UI or API to trigger ingestion (see developer guide for API details).

---

## 4. Remote Access (Optional)
- Use Ngrok to expose the UI or API for remote access:
  ```sh
  ngrok http --region=ap 3000
  ngrok http --region=ap 8001
  ```
- Use the provided public URL to access the chatbot remotely.

---

## 5. Common Issues
- If the UI does not load, check that all containers are running.
- For CORS or connection errors, see the Troubleshooting guide.

---

## 6. Getting Help
- See `TROUBLESHOOTING.md` for common problems.
- Contact your system administrator or developer for advanced issues.
