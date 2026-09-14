import re
import asyncio

with open('backend/scripts/benchmark_runner.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_loop = """
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
"""

text = re.sub(r'org_numbers = await fetch_random_companies\(100\).*?print\(f"Benchmark complete: \{results\}"\)', new_loop + '\n    print(f"Benchmark complete: {results}")', text, flags=re.DOTALL)

with open('backend/scripts/benchmark_runner.py', 'w', encoding='utf-8') as f:
    f.write(text)
print('Updated benchmark script for concurrent 1050 fetch!')
