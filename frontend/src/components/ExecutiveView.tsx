import React from 'react';
import { ProofPassport } from '../types';
import { formatCurrency, formatNumber, formatDate } from '../lib/utils';
import { Building2, MapPin, Users, Target, ArrowRight, Briefcase } from 'lucide-react';

export function ExecutiveView({ passport }: { passport: ProofPassport }) {
  const financial = passport.financial_summary?.statements?.[0];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
      
      {/* Identity Card */}
      <div className="bg-[var(--color-graphite-800)] p-5 rounded-lg border border-[var(--color-graphite-600)] col-span-1 lg:col-span-2">
        <h3 className="text-[var(--color-graphite-300)] font-mono text-sm mb-4 flex items-center gap-2 uppercase tracking-wide">
          <Building2 className="w-4 h-4" /> Company Identity
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <div className="text-[var(--color-graphite-400)] text-xs mb-1">Legal Name</div>
            <div className="text-[var(--color-graphite-100)] font-medium">{passport.company_name}</div>
          </div>
          <div>
            <div className="text-[var(--color-graphite-400)] text-xs mb-1">Organization Type</div>
            <div className="text-[var(--color-graphite-100)] font-medium">{passport.organization_type || '-'}</div>
          </div>
          <div>
            <div className="text-[var(--color-graphite-400)] text-xs mb-1">Incorporation Date</div>
            <div className="text-[var(--color-graphite-100)] font-medium">
              {formatDate(passport.facts.find(f => f.fact_type === 'incorporation_date')?.display_value || null)}
            </div>
          </div>
          <div>
            <div className="text-[var(--color-graphite-400)] text-xs mb-1">Share Capital</div>
            <div className="text-[var(--color-graphite-100)] font-medium">
              {formatCurrency(passport.facts.find(f => f.fact_type === 'share_capital')?.value_numeric || null)}
            </div>
          </div>
        </div>
      </div>

      {/* Primary Address */}
      <div className="bg-[var(--color-graphite-800)] p-5 rounded-lg border border-[var(--color-graphite-600)]">
        <h3 className="text-[var(--color-graphite-300)] font-mono text-sm mb-4 flex items-center gap-2 uppercase tracking-wide">
          <MapPin className="w-4 h-4" /> Registered Address
        </h3>
        {passport.addresses.filter(a => a.address_type === 'business').map((addr, idx) => (
          <div key={idx} className="text-[var(--color-graphite-100)] text-sm leading-relaxed">
            {addr.street_lines.map((line, i) => <div key={i}>{line}</div>)}
            <div>{addr.postal_code} {addr.city}</div>
            <div className="text-[var(--color-graphite-400)] mt-1">{addr.municipality_name}</div>
          </div>
        ))}
        {passport.addresses.length === 0 && <span className="text-[var(--color-graphite-500)] italic">No address recorded</span>}
      </div>

      {/* Financial Highlights */}
      <div className="bg-[var(--color-graphite-800)] p-5 rounded-lg border border-[var(--color-graphite-600)] col-span-1 lg:col-span-2">
        <h3 className="text-[var(--color-graphite-300)] font-mono text-sm mb-4 flex items-center gap-2 uppercase tracking-wide">
          <Target className="w-4 h-4" /> Financial Highlights {financial ? `(${financial.fiscal_year})` : ''}
        </h3>
        {financial ? (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-[var(--color-graphite-400)] text-xs mb-1">Revenue</div>
              <div className="text-[var(--color-graphite-100)] font-mono text-lg">{formatCurrency(financial.revenue)}</div>
            </div>
            <div>
              <div className="text-[var(--color-graphite-400)] text-xs mb-1">Operating Profit</div>
              <div className={`font-mono text-lg ${financial.operating_profit && financial.operating_profit < 0 ? 'text-[var(--color-danger)]' : 'text-[var(--color-success)]'}`}>
                {formatCurrency(financial.operating_profit)}
              </div>
            </div>
            <div>
              <div className="text-[var(--color-graphite-400)] text-xs mb-1">Total Assets</div>
              <div className="text-[var(--color-graphite-100)] font-mono text-lg">{formatCurrency(financial.total_assets)}</div>
            </div>
            <div>
              <div className="text-[var(--color-graphite-400)] text-xs mb-1">Equity</div>
              <div className="text-[var(--color-graphite-100)] font-mono text-lg">{formatCurrency(financial.equity)}</div>
            </div>
          </div>
        ) : (
          <div className="text-[var(--color-graphite-500)] italic py-4">No financial data available</div>
        )}
      </div>

      {/* Industries */}
      <div className="bg-[var(--color-graphite-800)] p-5 rounded-lg border border-[var(--color-graphite-600)]">
        <h3 className="text-[var(--color-graphite-300)] font-mono text-sm mb-4 flex items-center gap-2 uppercase tracking-wide">
          <Briefcase className="w-4 h-4" /> Industries
        </h3>
        <div className="flex flex-col gap-3">
          {passport.industries.sort((a,b) => a.priority - b.priority).map((ind, i) => (
            <div key={i} className="flex gap-3">
              <span className="text-[var(--color-electric-bright)] font-mono text-sm shrink-0">{ind.nace_code}</span>
              <span className="text-[var(--color-graphite-100)] text-sm">{ind.nace_description}</span>
            </div>
          ))}
          {passport.industries.length === 0 && <span className="text-[var(--color-graphite-500)] italic">No industries recorded</span>}
        </div>
      </div>

      {/* Key Roles Summary */}
      <div className="bg-[var(--color-graphite-800)] p-5 rounded-lg border border-[var(--color-graphite-600)] col-span-1 lg:col-span-3">
        <h3 className="text-[var(--color-graphite-300)] font-mono text-sm mb-4 flex items-center gap-2 uppercase tracking-wide">
          <Users className="w-4 h-4" /> Key Personnel & Board
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {passport.roles.filter(r => !r.is_resigned).slice(0, 6).map((role, i) => (
            <div key={i} className="p-3 bg-[var(--color-graphite-900)] rounded border border-[var(--color-graphite-700)]">
              <div className="text-[var(--color-electric-bright)] text-xs font-semibold mb-1 uppercase">{role.role_type_description}</div>
              <div className="text-[var(--color-graphite-100)] text-sm">
                {role.person_first_name ? `${role.person_first_name} ${role.person_last_name}` : role.entity_name}
              </div>
            </div>
          ))}
        </div>
        {passport.roles.length === 0 && <div className="text-[var(--color-graphite-500)] italic">No roles recorded</div>}
      </div>

    </div>
  );
}
