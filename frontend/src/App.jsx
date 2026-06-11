import React, { useState } from 'react';
import { evaluateMagi } from './services/api';
import EvaluationForm from './components/EvaluationForm';
import TerminalLoader from './components/TerminalLoader';
import MagiMatrices from './components/MagiMatrices';
import MetaAuditor from './components/MetaAuditor';
import MagiInfo from './components/MagiInfo';

import nervLogo from '/nervlogo.png';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleEvaluation = async (context, query) => {
    setIsLoading(true);
    setResult(null);
    setError(null);
    try {
      const data = await evaluateMagi(context, query);
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred during MAGI evaluation.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-4 md:p-8 font-sans">
      <header className="flex justify-between items-center border-b-2 border-nerv-red pb-4 mb-8">
        <div className="flex items-center gap-4">
          <img src={nervLogo} alt="NERV" className="w-16 h-16 object-contain mix-blend-screen" />
          <h1 className="text-white text-4xl md:text-6xl font-serif font-black tracking-widest uppercase mechanically-compressed glow-text-red m-0">
            NERV COMMAND
          </h1>
        </div>
        <div className="hidden md:flex flex-col items-end">
          <div className="text-nerv-red font-mono text-lg font-bold animate-pulse">
            TOP SECRET
          </div>
          <div className="text-gray-300 font-mono text-[10px] mt-1 uppercase">
            Restricted Access Only
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto">
        <MagiInfo />
        <EvaluationForm onSubmit={handleEvaluation} isLoading={isLoading} />
        
        {error && (
          <div className="border-l-4 border-nerv-red bg-nerv-red/10 p-4 mb-8 font-mono text-nerv-red">
            [ SYSTEM ERROR ] {error}
          </div>
        )}

        {isLoading && <TerminalLoader />}

        {result && !isLoading && (
          <div className="animate-[fadeIn_0.5s_ease-out]">
            <MagiMatrices data={result} />
            <MetaAuditor auditor={result.auditor} status={result.consensus_status} />
          </div>
        )}
      </main>
      
      <footer className="mt-20 border-t border-gray-800 pt-8 pb-4 text-center">
        <div className="text-gray-300 font-mono uppercase tracking-widest">
          God is in his heaven, all is right with the world
        </div>
      </footer>
    </div>
  );
}

export default App;
