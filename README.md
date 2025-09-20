# Project Setup Guide

This project ships with a Next.js front-end (`chat/`) and a FastAPI backend (`backend/`). Follow the steps below to run both services locally.

## Prerequisites
- Node.js 18+
- npm 9+ (bundled with Node.js)
- Python 3.11+

## Frontend (Next.js)
1. Open a terminal in the `chat/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. The app runs on `http://localhost:3000/` by default.

## Backend (FastAPI)
1. Open a terminal in the `backend/` directory.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Create a `.env` file in the `backend/` directory and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Launch the API server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 5002
   ```
6. The API exposes endpoints under `http://localhost:5002/`.

Stop the servers with `Ctrl+C` when you are finished.
