import React from 'react';
import { ProofPassport } from '../types';
import { AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

export function AuditView({ passport }: { passport: ProofPassport }) {
  const match = passport.identity_match;
  
  return (
    <div className="p-6 max-w-5xl mx-auto space-y-8">
      
      {/* Identity Firewall */}
      <section>
        <h2 className="text-xl font-bold text-[var(--color-graphite-100)] mb-4 uppercase tracking-widest border-b border-[var(--color-graphite-700)] pb-2 flex items-center gap-2">
          Identity Firewall Result
        </h2>
        
        <div className="bg-[var(--color-graphite-800)] border border-[var(--color-graphite-600)] rounded-lg overflow-hidden">
          <div className="p-5 border-b border-[var(--color-graphite-700)] flex justify-between items-center bg-[var(--color-graphite-900)]">
            <div>
              <div className="text-sm text-[var(--color-graphite-400)] mb-1">Target Identity</div>
              <div className="text-[var(--color-graphite-100)] font-mono text-lg">{match.canonical_name || match.candidate_name} ({match.organization_number})</div>
            </div>
            <div className="text-right">
              <div className="text-sm text-[var(--color-graphite-400)] mb-1">Decision</div>
              <div className={`text-xl font-bold font-mono ${match.decision === 'VERIFIED' ? 'text-[var(--color-success)]' : match.decision === 'REJECTED' ? 'text-[var(--color-danger)]' : 'text-[var(--color-warning)]'}`}>
                {match.decision}
              </div>
            </div>
          </div>
          
          <div className="p-5 text-sm text-[var(--color-graphite-200)] leading-relaxed">
            <strong>Reasoning:</strong> {match.reasoning}
          </div>

          {(match.matched_signals.length > 0 || match.conflicting_signals.length > 0) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-[var(--color-graphite-700)] border-t border-[var(--color-graphite-700)]">
              <div className="bg-[var(--color-graphite-800)] p-5">
                <h3 className="text-[var(--color-success)] text-sm font-bold mb-3 flex items-center gap-2 uppercase">
                  <CheckCircle className="w-4 h-4" /> Supporting Signals
                </h3>
                <ul className="space-y-3">
                  {match.matched_signals.map((sig, i) => (
                    <li key={i} className="text-sm border-l-2 border-[var(--color-success)] pl-3">
                      <div className="text-[var(--color-graphite-100)] font-medium capitalize">{sig.signal_type.replace(/_/g, ' ')}</div>
                      <div className="text-[var(--color-graphite-400)] font-mono text-xs mt-1">Found: {sig.found_value}</div>
                    </li>
                  ))}
                  {match.matched_signals.length === 0 && <li className="text-[var(--color-graphite-500)] text-sm italic">None</li>}
                </ul>
              </div>
              <div className="bg-[var(--color-graphite-800)] p-5">
                <h3 className="text-[var(--color-danger)] text-sm font-bold mb-3 flex items-center gap-2 uppercase">
                  <XCircle className="w-4 h-4" /> Conflicting Signals
                </h3>
                <ul className="space-y-3">
                  {match.conflicting_signals.map((sig, i) => (
                    <li key={i} className="text-sm border-l-2 border-[var(--color-danger)] pl-3">
                      <div className="text-[var(--color-graphite-100)] font-medium capitalize">{sig.signal_type.replace(/_/g, ' ')}</div>
                      <div className="text-[var(--color-graphite-400)] font-mono text-xs mt-1">Expected: {sig.expected_value} | Found: {sig.found_value}</div>
                    </li>
                  ))}
                  {match.conflicting_signals.length === 0 && <li className="text-[var(--color-graphite-500)] text-sm italic">None</li>}
                </ul>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* Conflicts Table */}
      <section>
        <h2 className="text-xl font-bold text-[var(--color-graphite-100)] mb-4 uppercase tracking-widest border-b border-[var(--color-graphite-700)] pb-2 flex items-center gap-2">
          Detected Conflicts
        </h2>
        {passport.conflicts.length === 0 ? (
          <div className="bg-[var(--color-graphite-800)] p-5 rounded-lg border border-[var(--color-graphite-600)] text-center text-[var(--color-success)] flex items-center justify-center gap-2">
            <CheckCircle className="w-5 h-5" /> No conflicts detected across sources.
          </div>
        ) : (
          <div className="space-y-4">
            {passport.conflicts.map((conf, i) => (
              <div key={i} className="bg-[var(--color-graphite-800)] p-5 rounded-lg border border-[var(--color-warning)] shadow-[0_0_10px_rgba(245,158,11,0.05)]">
                <div className="flex items-center gap-2 text-[var(--color-warning)] font-bold text-sm uppercase mb-3 border-b border-[var(--color-graphite-700)] pb-2">
                  <AlertTriangle className="w-4 h-4" /> {conf.fact_type.replace(/_/g, ' ')}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  {conf.values.map((v, idx) => (
                    <div key={idx} className="bg-[var(--color-graphite-900)] p-3 rounded border border-[var(--color-graphite-700)]">
                      <div className="text-[var(--color-graphite-100)] font-mono text-sm mb-1">{v.value}</div>
                      <div className="text-xs text-[var(--color-graphite-400)]">Source: {v.source} ({v.date})</div>
                    </div>
                  ))}
                </div>
                {conf.resolution && (
                  <div className="bg-[var(--color-graphite-900)] p-3 rounded border border-[var(--color-success)] text-sm">
                    <strong className="text-[var(--color-success)]">Resolution:</strong> <span className="text-[var(--color-graphite-100)] font-mono">{conf.resolution}</span>
                    <div className="text-[var(--color-graphite-400)] mt-1">{conf.resolution_reasoning}</div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </section>

    </div>
  );
}
