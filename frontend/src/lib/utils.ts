import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(n: number | null): string {
  if (n === null || n === undefined) return '-';
  return new Intl.NumberFormat('no-NO').format(n);
}

export function formatCurrency(n: number | null, currency: string = 'NOK'): string {
  if (n === null || n === undefined) return '-';
  return new Intl.NumberFormat('no-NO', { style: 'currency', currency, maximumFractionDigits: 0 }).format(n);
}

export function formatDate(d: string | null): string {
  if (!d) return '-';
  return new Date(d).toLocaleDateString('no-NO', { year: 'numeric', month: '2-digit', day: '2-digit' });
}

export function freshnessColor(status: string): string {
  switch (status.toUpperCase()) {
    case 'CURRENT': return 'bg-[var(--color-success)]';
    case 'RECENT': return 'bg-[var(--color-electric)]';
    case 'AGING': return 'bg-[var(--color-warning)]';
    case 'STALE': return 'bg-[var(--color-danger)]';
    default: return 'bg-[var(--color-graphite-400)]';
  }
}

export function confidenceColor(confidence: number): string {
  if (confidence >= 0.9) return 'bg-[var(--color-success)]';
  if (confidence >= 0.7) return 'bg-[var(--color-electric)]';
  if (confidence >= 0.5) return 'bg-[var(--color-warning)]';
  return 'bg-[var(--color-danger)]';
}

export function formatOrgNumber(n: string): string {
  if (!n || n.length !== 9) return n;
  return `${n.slice(0, 3)} ${n.slice(3, 6)} ${n.slice(6, 9)}`;
}
