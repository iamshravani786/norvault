import React from 'react';
import { ProofPassport } from '../types';
import { Activity, ArrowRight } from 'lucide-react';
import { confidenceColor } from '../lib/utils';

export function ChangeRadar({ passport }: { passport: ProofPassport }) {
  const changes = passport.changes_detected || [];

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="bg-[var(--color-graphite-800)] border border-[var(--color-graphite-600)] rounded-lg overflow-hidden">
        <div className="p-4 border-b border-[var(--color-graphite-700)] bg-[var(--color-graphite-900)] flex items-center gap-2">
          <Activity className="w-5 h-5 text-[var(--color-electric-bright)]" />
          <h2 className="text-[var(--color-graphite-100)] font-bold uppercase tracking-widest text-sm">Change Radar</h2>
        </div>
        
        {changes.length === 0 ? (
          <div className="p-8 text-center text-[var(--color-graphite-500)] italic">
            No recent changes detected for this entity.
          </div>
        ) : (
          <div className="divide-y divide-[var(--color-graphite-700)]">
            {changes.map((change, i) => (
              <div key={i} className="p-4 hover:bg-[var(--color-graphite-700)] transition-colors flex flex-col md:flex-row gap-4 justify-between items-start md:items-center">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-0.5 bg-[var(--color-graphite-900)] text-[var(--color-electric-bright)] border border-[var(--color-graphite-700)] rounded text-xs font-mono font-bold uppercase">
                      {change.change_type}
                    </span>
                    <span className="text-[var(--color-graphite-100)] font-mono text-sm">{change.field}</span>
                  </div>
                  
                  <div className="flex items-center gap-3 text-sm font-mono bg-[var(--color-graphite-900)] p-2 rounded border border-[var(--color-graphite-700)]">
                    {change.old_value ? (
                      <span className="text-[var(--color-danger)] line-through opacity-80 break-all">{change.old_value}</span>
                    ) : (
                      <span className="text-[var(--color-graphite-500)] italic">None</span>
                    )}
                    <ArrowRight className="w-4 h-4 text-[var(--color-graphite-400)] shrink-0" />
                    {change.new_value ? (
                      <span className="text-[var(--color-success)] break-all">{change.new_value}</span>
                    ) : (
                      <span className="text-[var(--color-graphite-500)] italic">None</span>
                    )}
                  </div>
                </div>
                
                <div className="flex flex-col items-end gap-1 text-right text-xs">
                  <div className="text-[var(--color-graphite-400)] font-mono">Source: <span className="text-[var(--color-graphite-200)]">{change.source}</span></div>
                  <div className="flex items-center gap-1 font-mono">
                    <div className={`w-2 h-2 rounded-full ${confidenceColor(change.confidence)}`}></div>
                    <span className="text-[var(--color-graphite-300)]">Conf: {Math.round(change.confidence * 100)}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
