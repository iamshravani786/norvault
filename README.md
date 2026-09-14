# NORVAULT

**Competition-grade Norwegian Company Intelligence Engine**

NORVAULT is a specialized intelligence pipeline that verifies Norwegian corporate facts using authoritative, publicly available government endpoints (BRREG). It employs adversarial auditing and contradiction detection to structurally prevent "hallucinations" (wrong-company claims and fabricated financial values) making it fully competition-ready.

## Features
- **Deterministic Pipeline**: Facts are mathematically linked to source bytes, not LLM guesses.
- **Identity Firewall**: Guarantees the correct legal entity is queried.
- **Adversarial Auditor**: Cross-checks fetched claims for structural consistency.
- **Evidence Graph**: Renders a complete traceability graph from source to fact.
- **Web Speech AI Assistant**: Navigate passports and query companies hands-free using Web Speech AI.

## Getting Started

### Backend
\\\ash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
\\\

### Frontend
\\\ash
cd frontend
npm install
npm run dev
\\\

## Architecture
See \AGENT.md\ and \COMPETITION.md\ for deep-dives into the verification logic and defense systems.
