import React from 'react';
import { ProofPassport } from '../types';
import { formatDate } from '../lib/utils';
import { Clock, ArrowRight } from 'lucide-react';

export function Timeline({ passport }: { passport: ProofPassport }) {
  const events = [...passport.timeline].sort((a, b) => {
    if (!a.event_date) return 1;
    if (!b.event_date) return -1;
    return new Date(b.event_date).getTime() - new Date(a.event_date).getTime();
  });

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="relative border-l-2 border-[var(--color-graphite-700)] ml-4 space-y-8 pb-8">
        {events.length === 0 && (
          <div className="text-[var(--color-graphite-500)] italic pl-8 py-8">No historical events recorded.</div>
        )}
        
        {events.map((evt, idx) => (
          <div key={idx} className="relative pl-8">
            <div className="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-[var(--color-graphite-800)] border-2 border-[var(--color-electric)] ring-4 ring-[var(--color-graphite-950)]" />
            
            <div className="bg-[var(--color-graphite-800)] rounded-lg p-5 border border-[var(--color-graphite-600)] shadow-sm hover:border-[var(--color-graphite-500)] transition-colors">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-3">
                <span className="px-2.5 py-1 text-xs font-bold font-mono bg-[var(--color-graphite-900)] text-[var(--color-electric-bright)] rounded uppercase border border-[var(--color-graphite-700)]">
                  {evt.event_type.replace(/_/g, ' ')}
                </span>
                <span className="text-sm font-mono text-[var(--color-graphite-300)] flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5" />
                  {formatDate(evt.event_date)}
                </span>
              </div>
              
              <div className="text-[var(--color-graphite-100)] text-sm mb-3">
                {evt.description || `Change in ${evt.event_type}`}
              </div>

              {(evt.old_value || evt.new_value) && (
                <div className="flex items-center gap-3 text-xs font-mono bg-[var(--color-graphite-900)] p-3 rounded border border-[var(--color-graphite-700)]">
                  {evt.old_value && (
                    <span className="text-[var(--color-danger)] line-through opacity-80 break-all">{evt.old_value}</span>
                  )}
                  {evt.old_value && evt.new_value && (
                    <ArrowRight className="w-4 h-4 text-[var(--color-graphite-400)] shrink-0" />
                  )}
                  {evt.new_value && (
                    <span className="text-[var(--color-success)] break-all">{evt.new_value}</span>
                  )}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
