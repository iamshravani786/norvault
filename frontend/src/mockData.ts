import { ProofPassport } from './types';

export const mockPassport: ProofPassport = {
  company_name: 'MOCK COMPANY AS',
  organization_number: '923609016',
  organization_type: 'AS',
  status: 'ACTIVE',
  identity_confidence: 0.98,
  last_verified: new Date().toISOString(),
  proof_score: 85,
  facts: [
    {
      id: 1,
      fact_type: 'incorporation_date',
      subject: '923609016',
      predicate: 'was_incorporated_on',
      display_value: '2019-10-15',
      value_numeric: null,
      source_name: 'Brønnøysundregistrene',
      source_url: 'https://brreg.no',
      source_date: '2019-10-15',
      retrieved_at: new Date().toISOString(),
      freshness_status: 'CURRENT',
      confidence: 1.0,
      identity_match_score: 1.0,
      fact_category: 'registration',
      why_this_company: 'Exact org number match.'
    }
  ],
  financial_summary: {
    statements: [
      {
        fiscal_year: 2022,
        statement_type: 'ANNUAL',
        currency: 'NOK',
        revenue: 15000000,
        operating_profit: 2000000,
        net_income: 1500000,
        total_assets: 10000000,
        equity: 4000000,
        total_debt: 6000000,
        source_name: 'Brønnøysundregistrene',
        source_url: 'https://brreg.no'
      }
    ],
    latest_year: 2022,
    has_group_accounts: false
  },
  roles: [],
  addresses: [
    {
      address_type: 'business',
      street_lines: ['Mockveien 1'],
      postal_code: '0101',
      city: 'Oslo',
      municipality_name: 'Oslo'
    }
  ],
  industries: [
    {
      priority: 1,
      nace_code: '62.010',
      nace_description: 'Programmeringstjenester'
    }
  ],
  parent: null,
  subsidiaries: [],
  identity_match: {
    organization_number: '923609016',
    canonical_name: 'MOCK COMPANY AS',
    candidate_name: 'MOCK COMPANY AS',
    match_score: 1.0,
    matched_signals: [],
    conflicting_signals: [],
    decision: 'VERIFIED',
    reasoning: 'Exact match on org number and name.'
  },
  conflicts: [],
  timeline: [],
  evidence_graph: { nodes: [], edges: [] },
  sources_consulted: [],
  changes_detected: [],
  run_id: 'mock-run-1',
  retrieval_time_sec: 1.2,
  requests_made: 5,
  cache_hits: 3
};
