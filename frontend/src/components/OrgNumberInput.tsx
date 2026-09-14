import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { cn, formatOrgNumber } from '../lib/utils';

interface Props {
  onSearch: (orgNumber: string) => void;
  isLoading?: boolean;
}

export function OrgNumberInput({ onSearch, isLoading }: Props) {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');

  const validateChecksum = (orgNo: string) => {
    if (orgNo.length !== 9) return false;
    const weights = [3, 2, 7, 6, 5, 4, 3, 2];
    let sum = 0;
    for (let i = 0; i < 8; i++) {
      sum += parseInt(orgNo[i]) * weights[i];
    }
    const remainder = sum % 11;
    const checkDigit = remainder === 0 ? 0 : 11 - remainder;
    return checkDigit === parseInt(orgNo[8]) && checkDigit !== 10;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value.replace(/\D/g, '').slice(0, 9);
    setValue(val);
    if (val.length === 9) {
      if (validateChecksum(val)) {
        setError('');
        onSearch(val);
      } else {
        setError('Invalid organization number checksum');
      }
    } else {
      setError('');
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 9);
    if (pasted.length === 9 && validateChecksum(pasted)) {
      setValue(pasted);
      setError('');
      onSearch(pasted);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (value.length === 9 && validateChecksum(value)) {
      onSearch(value);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-md mx-auto">
      <div className={cn(
        "relative flex items-center p-1 rounded-lg border",
        error ? "border-[var(--color-danger)]" : "border-[var(--color-electric)] bg-[var(--color-graphite-800)]"
      )}>
        <Search className="w-5 h-5 text-[var(--color-graphite-300)] ml-3 mr-2" />
        <input
          type="text"
          value={formatOrgNumber(value)}
          onChange={handleChange}
          onPaste={handlePaste}
          placeholder="Organization Number (9 digits)"
          className="flex-1 bg-transparent text-[var(--color-graphite-100)] font-mono text-lg p-2 outline-none placeholder-[var(--color-graphite-500)]"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || value.length !== 9 || !!error}
          className="px-4 py-2 bg-[var(--color-electric)] text-[var(--color-graphite-100)] rounded-md font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-[var(--color-electric-bright)] transition-colors"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>
      {error && <p className="text-[var(--color-danger)] text-sm mt-2 ml-1">{error}</p>}
    </form>
  );
}
