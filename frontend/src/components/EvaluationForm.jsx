import React, { useState } from 'react';

export default function EvaluationForm({ onSubmit, isLoading }) {
  const [context, setContext] = useState('');
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (context && query && !isLoading) {
      onSubmit(context, query);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-16">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        
        {/* Background Context Box */}
        <div className="flex flex-col border border-nerv-orange/50 bg-[#08080a] p-6 shadow-lg">
          <label className="text-nerv-orange font-sans font-bold uppercase tracking-wider text-sm flex items-center gap-2">
           Background Context
          </label>
          <div className="mt-4 bg-[#0e0e11] border border-gray-800 flex-1 p-5 shadow-inner group focus-within:border-nerv-orange/50 transition-colors">
            <textarea
              className="w-full h-32 md:h-40 bg-transparent text-gray-100 font-sans text-lg focus:outline-none resize-none"
              placeholder="Enter the background state of the problem..."
              value={context}
              onChange={(e) => setContext(e.target.value)}
              disabled={isLoading}
              required
            />
          </div>
        </div>

        {/* Dynamic Query Box */}
        <div className="flex flex-col border border-nerv-green/50 bg-[#08080a] p-6 shadow-lg">
          <label className="text-nerv-green font-sans font-bold uppercase tracking-wider text-sm flex items-center gap-2">
            Query
          </label>
          <div className="mt-4 bg-[#0e0e11] border border-gray-800 flex-1 p-5 shadow-inner group focus-within:border-nerv-green/50 transition-colors">
            <textarea
              className="w-full h-32 md:h-40 bg-transparent text-gray-100 font-sans text-lg focus:outline-none resize-none"
              placeholder="Enter the specific decision being asked..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={isLoading}
              required
            />
          </div>
        </div>

      </div>
      
      <div className="flex justify-center mt-6">
        <button
          type="submit"
          disabled={isLoading}
          className="relative overflow-hidden group bg-nerv-red px-16 py-6 text-xl md:text-2xl font-sans font-black uppercase text-black hover:bg-white hover:text-nerv-red shadow-[0_10px_30px_rgba(211,0,0,0.4)] cursor-pointer transition-all duration-300 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          style={{ clipPath: 'polygon(30px 0, 100% 0, 100% calc(100% - 30px), calc(100% - 30px) 100%, 0 100%, 0 30px)' }}
        >
          <span className="relative z-10 tracking-widest drop-shadow-sm">
            Initiate Magi Evaluation
          </span>
        </button>
      </div>
    </form>
  );
}
