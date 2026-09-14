import React from 'react';
import { ProofPassport } from '../types';
import { formatOrgNumber, formatDate } from '../lib/utils';
import { ShieldCheck, ShieldAlert, ShieldX } from 'lucide-react';

export function PassportHeader({ passport }: { passport: ProofPassport }) {
  const getStatusColor = (status: string) => {
    switch (status.toUpperCase()) {
      case 'ACTIVE': return 'bg-[var(--color-success)] text-[var(--color-graphite-100)]';
      case 'DISSOLVED':
      case 'BANKRUPT': return 'bg-[var(--color-danger)] text-[var(--color-graphite-100)]';
      case 'LIQUIDATING': return 'bg-[var(--color-warning)] text-[var(--color-graphite-100)]';
      default: return 'bg-[var(--color-graphite-500)] text-[var(--color-graphite-100)]';
    }
  };

  const renderConfidence = () => {
    const pct = Math.round(passport.identity_confidence * 100);
    let color = 'text-[var(--color-success)]';
    let Icon = ShieldCheck;
    if (pct < 70) { color = 'text-[var(--color-warning)]'; Icon = ShieldAlert; }
    if (pct < 40) { color = 'text-[var(--color-danger)]'; Icon = ShieldX; }

    return (
      <div className={`flex items-center gap-2 ${color} font-mono bg-[var(--color-graphite-800)] px-3 py-1.5 rounded-md border border-[var(--color-graphite-700)]`}>
        <Icon className="w-5 h-5" />
        <span>IDENTITY MATCH: {pct}%</span>
      </div>
    );
  };

  return (
    <div className="w-full bg-[var(--color-graphite-800)] border-b border-[var(--color-graphite-600)] p-6">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h1 className="text-3xl font-bold text-[var(--color-graphite-100)] tracking-tight">{passport.company_name}</h1>
            {passport.organization_type && (
              <span className="px-2 py-0.5 text-xs font-bold bg-[var(--color-graphite-700)] text-[var(--color-graphite-200)] rounded">
                {passport.organization_type}
              </span>
            )}
          </div>
          <div className="flex items-center gap-4 text-[var(--color-graphite-300)] font-mono">
            <span className="text-[var(--color-electric-bright)] text-xl">
              {formatOrgNumber(passport.organization_number)}
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase ${getStatusColor(passport.status)}`}>
              {passport.status}
            </span>
          </div>
        </div>

        <div className="flex flex-col items-end gap-3">
          {renderConfidence()}
          <div className="flex flex-col items-end text-sm text-[var(--color-graphite-400)] font-mono">
            <span>PROOF SCORE: <strong className="text-[var(--color-graphite-100)]">{passport.proof_score}/100</strong></span>
            <span>VERIFIED: {formatDate(passport.last_verified)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
