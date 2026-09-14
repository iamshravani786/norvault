import { useState, useEffect } from 'react';
import { Terminal, Database, Server, CheckCircle, ShieldAlert } from 'lucide-react';

interface ReplayStep {
  icon: 'server' | 'database' | 'shield' | 'check';
  title: string;
  color: string;
  lines: string[];
}

const STEPS: ReplayStep[] = [
  {
    icon: 'server', title: '1. SOURCE_FETCH', color: 'text-blue-400',
    lines: [
      'Initiating HTTP GET to BRREG Open API...',
      'GET https://data.brreg.no/enhetsregisteret/api/enheter/ HTTP/1.1',
      '200 OK (application/json) — Content verified',
    ],
  },
  {
    icon: 'database', title: '2. FACT_EXTRACTION', color: 'text-purple-400',
    lines: [
      'Parsing JSON payload & mapping to typed schema...',
      'Extracted field: organisasjonsnummer, navn, organisasjonsform',
      'Normalized Value: mapped to ExtractedFact model',
    ],
  },
  {
    icon: 'shield', title: '3. IDENTITY_FIREWALL', color: 'text-orange-400',
    lines: [
      'Cross-referencing entity attributes...',
      'Match Score: 1.00 (VERIFIED)',
      'Adversarial Auditor: PASSED — No temporal conflicts',
    ],
  },
  {
    icon: 'check', title: '4. COMMIT_TO_LEDGER', color: 'text-green-400',
    lines: [
      'Fact published to ProofPassport.',
      'Evidence graph node created with SUPPORTED_BY edge.',
      'Freshness: CURRENT — retrieved within this session.',
    ],
  },
];

const ICONS = {
  server: Server,
  database: Database,
  shield: ShieldAlert,
  check: CheckCircle,
};

export function EvidenceReplay({ factId, onClose }: { factId: number; onClose: () => void }) {
  const [visibleStep, setVisibleStep] = useState(-1);

  useEffect(() => {
    const timers = STEPS.map((_, i) =>
      setTimeout(() => setVisibleStep(i), 800 * (i + 1))
    );
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <div className="fixed inset-0 bg-black/80 z-[100] flex items-center justify-center p-4 backdrop-blur-sm">
      <div className="bg-[#0a0e1a] border border-[#1e3a8a]/40 w-full max-w-2xl rounded-xl shadow-[0_0_60px_rgba(30,58,138,0.2)] flex flex-col overflow-hidden">
        
        <div className="bg-[#0f1629] p-3 border-b border-[#1e3a8a]/30 flex items-center justify-between">
          <div className="flex items-center gap-2 text-green-400 font-mono text-xs">
            <Terminal size={14} />
            <span>NORVAULT PIPELINE REPLAY</span>
          </div>
          <button onClick={onClose} className="text-gray-500 hover:text-white transition-colors text-xl leading-none">&times;</button>
        </div>

        <div className="p-6 font-mono text-sm space-y-5 min-h-[340px]">
          <div className="text-gray-500 text-xs">
            {'>'} Initializing replay sequence for Fact #{factId}...
          </div>
          
          {STEPS.map((step, i) => {
            const Icon = ICONS[step.icon];
            return (
              <div
                key={i}
                className="transition-all duration-500"
                style={{
                  opacity: visibleStep >= i ? 1 : 0,
                  transform: visibleStep >= i ? 'translateY(0)' : 'translateY(16px)',
                }}
              >
                <div className="flex items-start gap-3">
                  <Icon size={18} className={`${step.color} mt-0.5 flex-shrink-0`} />
                  <div>
                    <div className={`${step.color} font-bold`}>{step.title}</div>
                    {step.lines.map((line, j) => (
                      <div key={j} className={j === 0 ? 'text-gray-400' : 'text-gray-600 text-xs'}>{line}</div>
                    ))}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
        
        {visibleStep >= 3 && (
          <div className="bg-[#0f1629] p-4 border-t border-[#1e3a8a]/30 flex justify-between items-center">
            <span className="text-green-400 text-xs font-mono">✓ All verification stages passed</span>
            <button 
              onClick={onClose}
              className="px-5 py-2 bg-[#1e3a8a] hover:bg-[#1e40af] text-white rounded text-sm font-medium transition-colors"
            >
              Acknowledge
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
