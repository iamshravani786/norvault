export interface ProofPassport {
  company_name: string
  organization_number: string
  organization_type: string | null
  status: string
  identity_confidence: number
  last_verified: string
  proof_score: number
  facts: PublishedFact[]
  financial_summary: FinancialSummary | null
  roles: CompanyRole[]
  addresses: CompanyAddress[]
  industries: CompanyIndustry[]
  parent: CompanyBrief | null
  subsidiaries: CompanyBrief[]
  identity_match: IdentityMatchResult
  conflicts: Conflict[]
  timeline: CompanyEvent[]
  evidence_graph: EvidenceGraphData
  sources_consulted: SourceConsulted[]
  changes_detected: ChangeDetected[]
  run_id: string
  retrieval_time_sec: number
  requests_made: number
  cache_hits: number
}

export interface PublishedFact {
  id: number
  fact_type: string
  subject: string
  predicate: string
  display_value: string
  value_numeric: number | null
  source_name: string
  source_url: string
  source_date: string | null
  retrieved_at: string
  freshness_status: string
  confidence: number
  identity_match_score: number
  fact_category: string
  why_this_company: string
}

export interface IdentityMatchResult {
  organization_number: string
  canonical_name: string
  candidate_name: string | null
  match_score: number
  matched_signals: IdentitySignal[]
  conflicting_signals: IdentitySignal[]
  decision: 'VERIFIED' | 'PROBABLE' | 'AMBIGUOUS' | 'REJECTED'
  reasoning: string
}

export interface IdentitySignal {
  signal_type: string
  expected_value: string | null
  found_value: string | null
  matches: boolean
  confidence: number
}

export interface CompanyRole {
  role_type_code: string
  role_type_description: string
  person_first_name: string | null
  person_last_name: string | null
  person_birth_date: string | null
  is_resigned: boolean
  entity_name: string | null
}

export interface CompanyAddress {
  address_type: string
  street_lines: string[]
  postal_code: string | null
  city: string | null
  municipality_name: string | null
}

export interface CompanyIndustry {
  priority: number
  nace_code: string
  nace_description: string | null
}

export interface CompanyBrief {
  org_number: string
  name: string
  org_form_code: string | null
}

export interface FinancialSummary {
  statements: FinancialStatement[]
  latest_year: number | null
  has_group_accounts: boolean
}

export interface FinancialStatement {
  fiscal_year: number
  statement_type: string
  currency: string
  revenue: number | null
  operating_profit: number | null
  net_income: number | null
  total_assets: number | null
  equity: number | null
  total_debt: number | null
  source_name: string
  source_url: string
}

export interface Conflict {
  fact_type: string
  values: { value: string; source: string; date: string }[]
  resolution: string | null
  resolution_reasoning: string | null
}

export interface CompanyEvent {
  event_type: string
  event_date: string | null
  description: string | null
  old_value: string | null
  new_value: string | null
}

export interface EvidenceGraphData {
  nodes: { id: string; node_type: string; label: string; data: Record<string, unknown> }[]
  edges: { source: string; target: string; edge_type: string; label: string }[]
}

export interface SourceConsulted {
  source_name: string
  source_url: string
  authority_level: number
  retrieved_at: string
  http_status: number | null
  facts_extracted: number
}

export interface ChangeDetected {
  change_type: string
  field: string
  old_value: string | null
  new_value: string | null
  source: string
  confidence: number
}

export interface BudgetStatus {
  requests_used: number
  requests_remaining: number
  requests_saved_by_cache: number
  cache_hit_rate: number
  external_cost_estimate: number
  cost_remaining: number
  budget_utilization_pct: number
}
