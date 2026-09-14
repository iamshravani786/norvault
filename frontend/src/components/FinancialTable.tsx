import React from 'react';
import { ProofPassport } from '../types';
import { formatCurrency } from '../lib/utils';
import { TrendingUp, TrendingDown } from 'lucide-react';

export function FinancialTable({ passport }: { passport: ProofPassport }) {
  const stats = passport.financial_summary?.statements || [];
  if (stats.length === 0) return <div className="text-[var(--color-graphite-500)] italic">No financials.</div>;
  
  const sortedStats = [...stats].sort((a, b) => b.fiscal_year - a.fiscal_year);
  
  return (
    <div className="overflow-x-auto border border-[var(--color-graphite-700)] rounded-lg">
      <table className="w-full text-right text-sm">
        <thead className="bg-[var(--color-graphite-900)] text-[var(--color-graphite-400)] text-xs uppercase font-mono">
          <tr>
            <th className="px-4 py-3 text-left">Metric</th>
            {sortedStats.map(s => <th key={s.fiscal_year} className="px-4 py-3">{s.fiscal_year}</th>)}
          </tr>
        </thead>
        <tbody className="divide-y divide-[var(--color-graphite-700)] bg-[var(--color-graphite-800)] text-[var(--color-graphite-100)] font-mono">
          {['Revenue', 'Operating Profit', 'Net Income', 'Total Assets', 'Equity', 'Total Debt'].map(metric => (
            <tr key={metric} className="hover:bg-[var(--color-graphite-700)] transition-colors">
              <td className="px-4 py-3 text-left font-sans text-[var(--color-graphite-200)]">{metric}</td>
              {sortedStats.map((s, i) => {
                let val: number | null = null;
                if (metric === 'Revenue') val = s.revenue;
                if (metric === 'Operating Profit') val = s.operating_profit;
                if (metric === 'Net Income') val = s.net_income;
                if (metric === 'Total Assets') val = s.total_assets;
                if (metric === 'Equity') val = s.equity;
                if (metric === 'Total Debt') val = s.total_debt;
                
                const isNeg = val !== null && val < 0;
                return (
                  <td key={s.fiscal_year} className={`px-4 py-3 cursor-pointer ${isNeg ? 'text-[var(--color-danger)]' : ''}`} title={`Source: ${s.source_name}`}>
                    {formatCurrency(val, s.currency)}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
