@echo off
echo Starting NORVAULT...
start cmd /k "cd backend && call .venv\Scripts\activate.bat && uvicorn app.main:app --host 0.0.0.0 --port 8000"
echo Backend started on http://localhost:8000
echo Frontend is pre-built and served as static files by the backend!
echo Navigate to http://localhost:8000 in your browser!
