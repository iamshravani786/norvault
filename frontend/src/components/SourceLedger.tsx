import React from 'react';
import { ProofPassport } from '../types';
import { formatDate } from '../lib/utils';
import { ExternalLink, Database } from 'lucide-react';

export function SourceLedger({ passport }: { passport: ProofPassport }) {
  const sources = [...passport.sources_consulted].sort((a, b) => b.authority_level - a.authority_level);

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="bg-[var(--color-graphite-800)] border border-[var(--color-graphite-600)] rounded-lg overflow-hidden">
        <div className="p-4 border-b border-[var(--color-graphite-700)] bg-[var(--color-graphite-900)] flex items-center gap-2">
          <Database className="w-5 h-5 text-[var(--color-electric-bright)]" />
          <h2 className="text-[var(--color-graphite-100)] font-bold uppercase tracking-widest text-sm">Source Ledger</h2>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-[var(--color-graphite-200)]">
            <thead className="text-xs uppercase bg-[var(--color-graphite-900)] text-[var(--color-graphite-400)] border-b border-[var(--color-graphite-700)]">
              <tr>
                <th className="px-4 py-3 font-mono">Source Name</th>
                <th className="px-4 py-3 font-mono">Authority</th>
                <th className="px-4 py-3 font-mono">Status</th>
                <th className="px-4 py-3 font-mono">Retrieved At</th>
                <th className="px-4 py-3 font-mono text-right">Facts</th>
              </tr>
            </thead>
            <tbody>
              {sources.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-[var(--color-graphite-500)] italic">
                    No sources consulted in this run.
                  </td>
                </tr>
              )}
              {sources.map((src, i) => (
                <tr key={i} className="border-b border-[var(--color-graphite-700)] hover:bg-[var(--color-graphite-700)] transition-colors">
                  <td className="px-4 py-3">
                    <a href={src.source_url} target="_blank" rel="noopener noreferrer" className="text-[var(--color-electric-bright)] hover:underline flex items-center gap-1.5 font-medium">
                      {src.source_name} <ExternalLink className="w-3 h-3" />
                    </a>
                  </td>
                  <td className="px-4 py-3">
                    <span className="bg-[var(--color-graphite-800)] px-2 py-1 rounded text-xs font-mono border border-[var(--color-graphite-600)]">
                      Lvl {src.authority_level}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-mono">
                    {src.http_status === 200 ? (
                      <span className="text-[var(--color-success)]">200 OK</span>
                    ) : src.http_status ? (
                      <span className="text-[var(--color-danger)]">{src.http_status} ERR</span>
                    ) : (
                      <span className="text-[var(--color-graphite-500)]">N/A</span>
                    )}
                  </td>
                  <td className="px-4 py-3 font-mono text-xs">{formatDate(src.retrieved_at)}</td>
                  <td className="px-4 py-3 font-mono text-right font-bold text-[var(--color-graphite-100)]">{src.facts_extracted}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
