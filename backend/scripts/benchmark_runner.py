import asyncio
import httpx
import time
import json
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.pipeline import CompanyPipeline
from app.database import init_db, async_session_factory
from app.api.deps import _budget_manager, _cache_manager, _http_client

async def fetch_random_companies(limit: int = 1050) -> list[str]:
    print(f"Fetching {limit} active Norwegian companies for benchmark...")
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://data.brreg.no/enhetsregisteret/api/enheter?organisasjonsform=AS&size={limit}")
        resp.raise_for_status()
        data = resp.json()
        enheter = data.get("_embedded", {}).get("enheter", [])
        org_numbers = [e["organisasjonsnummer"] for e in enheter]
        print(f"Loaded {len(org_numbers)} organizations.")
        return org_numbers

async def run_benchmark():
    await init_db()
    
    
    org_numbers = await fetch_random_companies(1050)
    
    results = {
        "total_companies": len(org_numbers),
        "successful": 0,
        "failed": 0
    }
    
    sem = asyncio.Semaphore(15)
    
    async def process_org(org):
        async with sem:
            print(f"Processing {org}...")
            try:
                async with async_session_factory() as session:
                    pipeline = CompanyPipeline(session, _http_client, _cache_manager, _budget_manager)
                    await pipeline.run(org)
                    await session.commit()
                results["successful"] += 1
                print(f"Success for {org}")
            except Exception as e:
                results["failed"] += 1
                print(f"Failed for {org}: {e}")

    await asyncio.gather(*(process_org(org) for org in org_numbers))

    print(f"Benchmark complete: {results}")

if __name__ == '__main__':
    asyncio.run(run_benchmark())
