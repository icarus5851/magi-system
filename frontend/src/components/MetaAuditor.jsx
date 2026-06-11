import React from 'react';

export default function MetaAuditor({ auditor, status }) {
  if (!auditor) return null;
  
  const getStatusTheme = (statusStr) => {
    const s = (statusStr || '').toUpperCase();
    if (s.includes('CONFLICT') || s.includes('DISAGREEMENT')) {
      return { text: 'text-nerv-red', border: 'border-nerv-red', shadow: 'shadow-[0_0_20px_rgba(211,0,0,0.3)]' };
    }
    if (s.includes('AGREEMENT') || s.includes('CONSENSUS')) {
      return { text: 'text-nerv-green', border: 'border-nerv-green', shadow: 'shadow-[0_0_20px_rgba(57,255,20,0.3)]' };
    }
    return { text: 'text-nerv-orange', border: 'border-nerv-orange', shadow: 'shadow-[0_0_20px_rgba(255,92,0,0.3)]' };
  };

  const theme = getStatusTheme(status);

  return (
    <div className={`border-2 p-8 md:p-12 bg-[#0c0c0e] ${theme.border} ${theme.shadow} relative overflow-hidden`}>
      {/* Background decoration */}
      <div className="absolute -right-10 -top-10 opacity-[0.03] pointer-events-none">
        <div className="text-[200px] font-serif mechanically-compressed font-black">MAGI</div>
      </div>

      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 border-b border-gray-800 pb-6 relative z-10">
        <h2 className="font-serif text-5xl md:text-6xl font-black uppercase mechanically-compressed text-white tracking-wide">
          Meta-Auditor
        </h2>
        <div className={`font-mono text-2xl md:text-3xl uppercase tracking-widest mt-4 md:mt-0 font-bold ${theme.text}`}>
          STATUS: {status}
        </div>
      </div>
      
      {auditor.mcp_trace_consulted && (
        <div className="mb-10 w-full animate-[slideDown_0.4s_ease-out_forwards] border border-cyan-500/50 bg-cyan-900/10 shadow-[0_0_25px_rgba(6,182,212,0.15)] relative z-10">
          <div className="bg-cyan-500 text-black px-5 py-2 font-sans font-black tracking-widest text-sm uppercase flex items-center gap-3">
            <span className="w-2 h-2 bg-black animate-pulse rounded-full"></span> LIVE MCP TOOL-CALL TRACE
          </div>
          <div className="p-6 font-mono text-cyan-400 text-base leading-relaxed border-l-4 border-cyan-500/50 ml-4 my-2">
            {auditor.trace_insight}
          </div>
        </div>
      )}
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 relative z-10">
        <div>
          <div className="font-sans font-bold text-sm text-white/70 uppercase tracking-widest mb-4">Final Master Solution</div>
          <div className="font-sans text-2xl md:text-3xl text-white leading-relaxed font-normal">
            {auditor.final_master_solution}
          </div>
        </div>
        
        <div className="flex flex-col">
          <div className="mb-8">
            <div className="font-sans font-bold text-sm text-white/70 uppercase tracking-widest mb-4">Conflict Summary</div>
            <div className="font-sans text-xl text-gray-200 leading-relaxed border-l-4 border-gray-600 pl-6 py-2">
              {auditor.conflict_summary}
            </div>
          </div>
          
          {auditor.system_correction && auditor.system_correction !== "NONE" && (
            <div className="mt-auto pt-6 border-t border-gray-800">
              <div className="font-sans font-bold text-sm text-nerv-red uppercase tracking-widest mb-3 glow-text-red">System Correction Logged</div>
              <div className="font-sans text-base text-white bg-nerv-red/20 border border-nerv-red/50 p-5 leading-relaxed font-medium">
                {auditor.system_correction}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
