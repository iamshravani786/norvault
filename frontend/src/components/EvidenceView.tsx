import React, { useMemo } from 'react';
import { ProofPassport } from '../types';
import { FactCard } from './FactCard';

export function EvidenceView({ passport }: { passport: ProofPassport }) {
  const groupedFacts = useMemo(() => {
    const groups: Record<string, typeof passport.facts> = {};
    passport.facts.forEach(fact => {
      const cat = fact.fact_category || 'other';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(fact);
    });
    return groups;
  }, [passport.facts]);

  const categories = Object.keys(groupedFacts).sort();

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-10">
      {categories.length === 0 && (
        <div className="text-center text-[var(--color-graphite-500)] py-20 italic">
          No discrete facts extracted for this entity.
        </div>
      )}
      
      {categories.map(category => (
        <section key={category}>
          <h2 className="text-xl font-bold text-[var(--color-graphite-100)] mb-4 uppercase tracking-widest border-b border-[var(--color-graphite-700)] pb-2 flex items-center gap-2">
            <span className="w-2 h-2 bg-[var(--color-electric)] rounded-full inline-block"></span>
            {category} Facts
            <span className="text-sm font-normal text-[var(--color-graphite-400)] ml-2">({groupedFacts[category].length})</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {groupedFacts[category].map(fact => (
              <FactCard key={fact.id} fact={fact} />
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}
