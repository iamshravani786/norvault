import React from 'react';
import { ProofPassport } from '../types';
import { Users } from 'lucide-react';
import { formatDate } from '../lib/utils';

export function RolesTable({ passport }: { passport: ProofPassport }) {
  const roles = passport.roles || [];

  return (
    <div className="bg-[var(--color-graphite-800)] border border-[var(--color-graphite-600)] rounded-lg overflow-hidden">
      <div className="p-4 border-b border-[var(--color-graphite-700)] bg-[var(--color-graphite-900)] flex items-center gap-2">
        <Users className="w-5 h-5 text-[var(--color-electric-bright)]" />
        <h2 className="text-[var(--color-graphite-100)] font-bold uppercase tracking-widest text-sm">Registered Roles</h2>
      </div>
      
      {roles.length === 0 ? (
        <div className="p-8 text-center text-[var(--color-graphite-500)] italic">
          No active or historical roles recorded.
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-[var(--color-graphite-200)]">
            <thead className="text-xs uppercase bg-[var(--color-graphite-900)] text-[var(--color-graphite-400)] border-b border-[var(--color-graphite-700)]">
              <tr>
                <th className="px-4 py-3 font-mono">Role Type</th>
                <th className="px-4 py-3 font-mono">Name / Entity</th>
                <th className="px-4 py-3 font-mono">Birth Date</th>
                <th className="px-4 py-3 font-mono">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--color-graphite-700)]">
              {roles.map((role, i) => (
                <tr key={i} className={`hover:bg-[var(--color-graphite-700)] transition-colors ${role.is_resigned ? 'opacity-50' : ''}`}>
                  <td className="px-4 py-3 font-mono font-medium text-[var(--color-electric-bright)]">
                    {role.role_type_description}
                  </td>
                  <td className="px-4 py-3 text-[var(--color-graphite-100)]">
                    {role.person_first_name 
                      ? `${role.person_first_name} ${role.person_last_name}` 
                      : role.entity_name}
                  </td>
                  <td className="px-4 py-3 font-mono text-xs">
                    {formatDate(role.person_birth_date)}
                  </td>
                  <td className="px-4 py-3">
                    {role.is_resigned ? (
                      <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-[var(--color-graphite-900)] text-[var(--color-graphite-400)] border border-[var(--color-graphite-700)]">RESIGNED</span>
                    ) : (
                      <span className="px-2 py-0.5 rounded text-xs font-mono font-bold bg-[var(--color-success)] text-[var(--color-graphite-100)]">ACTIVE</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
