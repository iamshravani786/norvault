import React, { useState } from 'react';
import { QueryClient, QueryClientProvider, useQuery } from '@tanstack/react-query';
import { OrgNumberInput } from './components/OrgNumberInput';
import { PassportHeader } from './components/PassportHeader';
import { ModeSelector, ViewMode } from './components/ModeSelector';
import { ExecutiveView } from './components/ExecutiveView';
import { EvidenceView } from './components/EvidenceView';
import { Timeline } from './components/Timeline';
import { EvidenceGraph } from './components/EvidenceGraph';
import { AuditView } from './components/AuditView';
import { BudgetPanel } from './components/BudgetPanel';
import { EvidenceReplay } from './components/EvidenceReplay';
import { SourceLedger } from './components/SourceLedger';
import { fetchPassport, fetchBudget } from './lib/api';
import { mockPassport } from './mockData';
import { VoiceAssistant } from './components/VoiceAssistant';
import { HelpSupportModal } from './components/HelpSupportModal';
import { Shield, HelpCircle } from 'lucide-react';

const queryClient = new QueryClient();

function MainDashboard() {
  const [orgNumber, setOrgNumber] = useState<string>('');
  const [mode, setMode] = useState<ViewMode>('EXECUTIVE');
  const [replayFactId, setReplayFactId] = useState<number | null>(null);
  const [isHelpOpen, setIsHelpOpen] = useState(false);

  const { data: passport, isLoading, isError, error } = useQuery({
    queryKey: ['passport', orgNumber],
    queryFn: () => fetchPassport(orgNumber),
    enabled: !!orgNumber,
    retry: false
  });

  const { data: budget } = useQuery({
    queryKey: ['budget'],
    queryFn: () => fetchBudget().catch(() => undefined),
  });

  return (
    <div className="min-h-screen bg-[var(--color-graphite-950)] text-[var(--color-graphite-100)] font-sans pb-20">
      {/* Top Navigation */}
      <header className="bg-[var(--color-graphite-900)] border-b border-[var(--color-graphite-700)] sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-8">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-[var(--color-electric)] rounded flex items-center justify-center font-bold text-white">N</div>
            <span className="font-mono font-bold text-xl tracking-widest text-[var(--color-graphite-100)] hidden sm:block">NORVAULT</span>
          </div>
          
          <div className="flex-1 max-w-xl">
            <OrgNumberInput onSearch={setOrgNumber} isLoading={isLoading} />
          </div>

          <div className="flex items-center gap-4">
            <button 
              onClick={() => setIsHelpOpen(true)}
              className="text-[var(--color-graphite-400)] hover:text-white transition-colors flex items-center gap-1"
              title="Help & Support"
            >
              <HelpCircle size={20} />
              <span className="hidden md:inline text-sm">Help</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="w-full">
        {!orgNumber ? (
          <div className="flex flex-col items-center justify-center h-[70vh] text-[var(--color-graphite-400)]">
            <div className="w-24 h-24 mb-6 opacity-20 border-4 border-current rounded-full border-t-transparent animate-spin" />
            <h2 className="text-2xl font-mono mb-2">Awaiting Target</h2>
            <p className="text-sm">Enter a 9-digit Norwegian organization number to begin intelligence extraction.</p>
          </div>
        ) : isLoading ? (
          <div className="flex flex-col items-center justify-center h-[50vh] text-[var(--color-electric)]">
            <div className="w-16 h-16 mb-6 border-4 border-current rounded-full border-t-transparent animate-spin" />
            <p className="font-mono animate-pulse">Compiling Proof Passport...</p>
          </div>
        ) : isError && !passport ? (
          <div className="p-8 text-center text-[var(--color-danger)]">
            <h2 className="text-xl font-bold mb-2">Extraction Failed</h2>
            <p className="font-mono">{(error as Error).message}</p>
          </div>
        ) : passport ? (
          <div className="animate-in fade-in duration-500">
            <PassportHeader passport={passport} />
            
            <div className="bg-[var(--color-graphite-900)] border-b border-[var(--color-graphite-700)] sticky top-16 z-30 px-6 py-3 shadow-md">
              <div className="max-w-7xl mx-auto flex justify-between items-center">
                <ModeSelector mode={mode} setMode={setMode} />
              </div>
            </div>

            <div className="mt-6">
              {mode === 'EXECUTIVE' && <ExecutiveView passport={passport} />}
              {mode === 'EVIDENCE' && <EvidenceView passport={passport} />}
              {mode === 'TIMELINE' && <Timeline passport={passport} />}
              {mode === 'GRAPH' && <EvidenceGraph passport={passport} />}
              {mode === 'AUDIT' && (
                <>
                  <AuditView passport={passport} />
                  <div className="mt-8 border-t border-[var(--color-graphite-700)] pt-8">
                    <SourceLedger passport={passport} />
                  </div>
                </>
              )}
            </div>
          </div>
        ) : null}
      </main>

      <BudgetPanel budget={budget} />
      
      {replayFactId !== null && (
        <EvidenceReplay factId={replayFactId} onClose={() => setReplayFactId(null)} />
      )}
      <VoiceAssistant 
        onCommand={setOrgNumber} 
        isProcessing={isLoading} 
      />
      <HelpSupportModal 
        isOpen={isHelpOpen} 
        onClose={() => setIsHelpOpen(false)} 
      />
    </div>
  );
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <MainDashboard />
    </QueryClientProvider>
  );
}

