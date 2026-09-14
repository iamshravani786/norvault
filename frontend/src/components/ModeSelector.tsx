import React from 'react';
import { Briefcase, Shield, Clock, Network, AlertTriangle } from 'lucide-react';
import { cn } from '../lib/utils';

export type ViewMode = 'EXECUTIVE' | 'EVIDENCE' | 'TIMELINE' | 'GRAPH' | 'AUDIT';

interface Props {
  mode: ViewMode;
  setMode: (mode: ViewMode) => void;
}

const MODES: { id: ViewMode; label: string; icon: React.ElementType }[] = [
  { id: 'EXECUTIVE', label: 'EXECUTIVE', icon: Briefcase },
  { id: 'EVIDENCE', label: 'EVIDENCE', icon: Shield },
  { id: 'TIMELINE', label: 'TIMELINE', icon: Clock },
  { id: 'GRAPH', label: 'GRAPH', icon: Network },
  { id: 'AUDIT', label: 'AUDIT', icon: AlertTriangle },
];

export function ModeSelector({ mode, setMode }: Props) {
  return (
    <div className="flex space-x-1 bg-[var(--color-graphite-900)] p-1 rounded-lg border border-[var(--color-graphite-700)] overflow-x-auto">
      {MODES.map(({ id, label, icon: Icon }) => (
        <button
          key={id}
          onClick={() => setMode(id)}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-md text-sm font-semibold transition-all duration-200",
            mode === id
              ? "bg-[var(--color-graphite-700)] text-[var(--color-electric-bright)] shadow-sm"
              : "text-[var(--color-graphite-400)] hover:text-[var(--color-graphite-200)] hover:bg-[var(--color-graphite-800)]"
          )}
        >
          <Icon className="w-4 h-4" />
          {label}
        </button>
      ))}
    </div>
  );
}
