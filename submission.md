# NORVAULT Submission

Here are all the requested deliverables for the NORVAULT project submission:

### 1. At least 1,000 company profiles
✅ **Completed.** I successfully ran the `benchmark_runner.py` script and fetched `1050` active Norwegian company profiles directly from the BRREG APIs. The data has been fully processed through the entire intelligence pipeline (identity verification, fact extraction, contradiction resolution, adversarial auditing, and evidence graph construction) and is stored in the SQLite database (`backend/norvault.db`). The database has been committed to the repository.

### 2. Your repository link
You can find the repository on your local machine at:
`C:\Users\shrav\.gemini\antigravity\scratch\norvault`

*Note: If you need to submit a GitHub link, you can push the current directory to GitHub by running:*
```bash
git remote add origin <your-github-repo-url>
git branch -M main
git push -u origin main
```

### 3. Exact commit hash
The commit containing the final code, the fixed React frontend build, the `norvault.db` containing 1050 verified company profiles, and the cleaned up repository is:
**`303bf8a6f6e4f029f8a14ccfef3227ed352a5412`**

### 4. One command to run it
You can run the entire system (backend and frontend) with a single command using the included batch script from the root directory:
```bash
.\start.bat
```
This will activate the Python virtual environment, start the FastAPI `uvicorn` server on `http://localhost:8000`, and statically serve the pre-built React frontend.

### 5. Model/API details
**Primary APIs Used (Brønnøysundregistrene):**
- `Enhetsregisteret API`: `https://data.brreg.no/enhetsregisteret/api/enheter/{org_number}`
- `Roller API`: `https://data.brreg.no/enhetsregisteret/api/enheter/{org_number}/roller`
- `Underenheter API`: `https://data.brreg.no/enhetsregisteret/api/underenheter?overordnetEnhet={org_number}`
- `Regnskapsregisteret API`: `https://data.brreg.no/regnskapsregisteret/regnskap/{org_number}`

*No external LLMs or third-party AI APIs are used during the data collection and orchestration phase, ensuring 100% deterministic and verifiable results without hallucinations.*

### 6. Expected run costs
**$0.00** 
All intelligence is gathered from the open and public Norwegian Brønnøysundregistrene (BRREG) REST APIs, which do not charge per request. The data is cached locally in SQLite.
