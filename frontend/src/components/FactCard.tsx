import React, { useState } from 'react';
import { PublishedFact } from '../types';
import { cn, formatDate, confidenceColor, freshnessColor } from '../lib/utils';
import { ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';

interface Props {
  fact: PublishedFact;
  onReplayClick?: (factId: number) => void;
}

export function FactCard({ fact, onReplayClick }: Props) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-[var(--color-graphite-800)] border border-[var(--color-graphite-600)] rounded-lg p-4 hover:border-[var(--color-graphite-500)] transition-colors">
      <div className="flex justify-between items-start mb-2">
        <span className="text-xs font-mono text-[var(--color-graphite-400)] uppercase tracking-wider">
          {fact.fact_type.replace(/_/g, ' ')}
        </span>
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1 text-xs font-mono text-[var(--color-graphite-300)]" title="Confidence">
            <span className={cn("w-2 h-2 rounded-full", confidenceColor(fact.confidence))} />
            {Math.round(fact.confidence * 100)}%
          </span>
          <span className={cn("px-1.5 py-0.5 rounded text-[10px] font-bold text-[var(--color-graphite-100)]", freshnessColor(fact.freshness_status))}>
            {fact.freshness_status}
          </span>
        </div>
      </div>
      
      <div className="text-lg font-semibold text-[var(--color-graphite-100)] mb-4 break-words">
        {fact.display_value}
      </div>
      
      <div className="flex flex-col gap-1 text-xs text-[var(--color-graphite-400)] font-mono border-t border-[var(--color-graphite-700)] pt-3">
        <div className="flex justify-between">
          <span>Source:</span>
          <a href={fact.source_url} target="_blank" rel="noopener noreferrer" className="text-[var(--color-electric-bright)] hover:underline flex items-center gap-1">
            {fact.source_name} <ExternalLink className="w-3 h-3" />
          </a>
        </div>
        <div className="flex justify-between">
          <span>Date:</span>
          <span className="text-[var(--color-graphite-200)]">{formatDate(fact.source_date)}</span>
        </div>
      </div>

      {(fact.why_this_company || onReplayClick) && (
        <div className="mt-3">
          <button
            onClick={() => setExpanded(!expanded)}
            className="flex items-center gap-1 text-xs text-[var(--color-graphite-400)] hover:text-[var(--color-graphite-200)] transition-colors"
          >
            {expanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            Evidence Details
          </button>
          
          {expanded && (
            <div className="mt-2 p-3 bg-[var(--color-graphite-900)] rounded border border-[var(--color-graphite-700)] text-xs text-[var(--color-graphite-300)]">
              {fact.why_this_company && (
                <div className="mb-2">
                  <strong className="text-[var(--color-graphite-200)] block mb-1">Identity Reasoning:</strong>
                  {fact.why_this_company}
                </div>
              )}
              {onReplayClick && (
                <button
                  onClick={() => onReplayClick(fact.id)}
                  className="mt-2 px-3 py-1.5 bg-[var(--color-graphite-700)] hover:bg-[var(--color-graphite-600)] text-[var(--color-graphite-100)] rounded transition-colors w-full text-center"
                >
                  View Evidence Replay
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
