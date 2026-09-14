import { BudgetStatus, ProofPassport } from '../types';

const BASE = '/api/v1';

export async function fetchPassport(orgNumber: string): Promise<ProofPassport> {
  const res = await fetch(`${BASE}/companies/${orgNumber}`, { headers: { "ngrok-skip-browser-warning": "true" } });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchBudget(): Promise<BudgetStatus> {
  const res = await fetch(`${BASE}/admin/budget`, { headers: { "ngrok-skip-browser-warning": "true" } });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function fetchEvidenceReplay(orgNumber: string, factId: number) {
  const res = await fetch(`${BASE}/companies/${orgNumber}/evidence/${factId}`, { headers: { "ngrok-skip-browser-warning": "true" } });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function searchCompanies(query: string) {
  const res = await fetch(`${BASE}/search?q=${encodeURIComponent(query)}`, { headers: { "ngrok-skip-browser-warning": "true" } });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}
