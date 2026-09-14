# Start the NORVAULT platform

echo "======================================"
echo "    Starting NORVAULT Platform"
echo "======================================"

# Check if uv is installed, use pip otherwise
$PYTHON_ENV = "pip"
if (Get-Command "uv" -ErrorAction SilentlyContinue) {
    $PYTHON_ENV = "uv"
}

# Start Backend
echo "Starting FastAPI Backend on port 8000..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; if (!(Test-Path .venv)) { python -m venv .venv }; .\.venv\Scripts\Activate.ps1; pip install -e .[dev]; uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

# Start Frontend
echo "Starting Vite Frontend on port 5173..."
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

echo "======================================"
echo "NORVAULT is starting in separate windows."
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "======================================"
