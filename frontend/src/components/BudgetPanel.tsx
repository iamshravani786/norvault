import React from 'react';
import { BudgetStatus } from '../types';
import { formatCurrency, formatNumber } from '../lib/utils';
import { Activity } from 'lucide-react';

export function BudgetPanel({ budget }: { budget?: BudgetStatus }) {
  if (!budget) return null;

  return (
    <div className="fixed bottom-6 right-6 w-72 bg-[var(--color-graphite-900)] border border-[var(--color-graphite-700)] rounded-lg shadow-2xl overflow-hidden z-50 opacity-90 hover:opacity-100 transition-opacity">
      <div className="bg-[var(--color-graphite-800)] px-4 py-2 border-b border-[var(--color-graphite-700)] flex items-center gap-2">
        <Activity className="w-4 h-4 text-[var(--color-electric-bright)]" />
        <span className="text-xs font-mono text-[var(--color-graphite-200)] uppercase font-bold tracking-wider">System Budget</span>
      </div>
      
      <div className="p-4 space-y-4">
        <div>
          <div className="flex justify-between text-xs text-[var(--color-graphite-400)] mb-1 font-mono">
            <span>Requests</span>
            <span>{formatNumber(budget.requests_used)} / {formatNumber(budget.requests_used + budget.requests_remaining)}</span>
          </div>
          <div className="w-full bg-[var(--color-graphite-800)] rounded-full h-1.5">
            <div 
              className={`h-1.5 rounded-full ${budget.budget_utilization_pct > 80 ? 'bg-[var(--color-danger)]' : 'bg-[var(--color-electric)]'}`} 
              style={{ width: `${Math.min(100, budget.budget_utilization_pct)}%` }}
            ></div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 text-xs font-mono">
          <div className="bg-[var(--color-graphite-800)] p-2 rounded">
            <div className="text-[var(--color-graphite-500)] mb-0.5">Cache Hit Rate</div>
            <div className="text-[var(--color-success)] font-bold">{Math.round(budget.cache_hit_rate * 100)}%</div>
          </div>
          <div className="bg-[var(--color-graphite-800)] p-2 rounded">
            <div className="text-[var(--color-graphite-500)] mb-0.5">Est. Cost</div>
            <div className="text-[var(--color-graphite-100)] font-bold">{formatCurrency(budget.external_cost_estimate)}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
