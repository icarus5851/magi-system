import React from 'react';

const MatrixCard = ({ name, title, data, colorName }) => {
  const colors = {
    blue: { border: 'border-blue-500', text: 'text-blue-500', bg: 'bg-blue-500' },
    yellow: { border: 'border-yellow-500', text: 'text-yellow-500', bg: 'bg-yellow-500' },
    orange: { border: 'border-nerv-orange', text: 'text-nerv-orange', bg: 'bg-nerv-orange' },
  };
  const c = colors[colorName];

  return (
    <div className={`border-2 ${c.border} bg-black/90 p-8 md:p-10 flex flex-col relative overflow-hidden group`}>
      {/* Background grid accent */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:20px_20px] pointer-events-none"></div>
      
      <h2 className={`font-serif text-4xl font-black uppercase mb-2 mechanically-compressed ${c.text}`}>
        {name}
      </h2>
      <div className="font-sans text-sm md:text-base font-bold tracking-widest text-white/90 mb-8 uppercase">
        {title}
      </div>
      
      <div className="mb-8 relative z-10">
        <div className="font-sans font-bold text-xs text-white/60 uppercase tracking-widest mb-2">Recommendation</div>
        <div className="font-sans text-white text-xl md:text-2xl font-medium leading-tight">{data.recommendation}</div>
      </div>
      
      <div className="mb-8 relative z-10">
        <div className="flex justify-between items-end mb-2">
          <div className="font-sans font-bold text-xs text-white/60 uppercase tracking-widest">Confidence Score</div>
          <div className={`font-mono text-lg font-bold ${c.text}`}>{data.confidence_score}%</div>
        </div>
        <div className="w-full h-3 bg-gray-900 border border-gray-700">
          <div className={`h-full ${c.bg} transition-all duration-1000 ease-out`} style={{ width: `${data.confidence_score}%` }}></div>
        </div>
      </div>
      
      <div className="mb-8 relative z-10">
        <div className="font-sans font-bold text-xs text-white/60 uppercase tracking-widest mb-2">Reasoning</div>
        <div className="font-sans text-gray-200 text-base leading-relaxed">{data.reasoning}</div>
      </div>
      
      <div className="mt-auto pt-6 border-t border-gray-800 relative z-10">
        <div className="font-sans font-bold text-xs text-nerv-red uppercase tracking-widest mb-2">Key Risk</div>
        <div className="font-sans text-nerv-red/90 text-base font-medium">{data.key_risk}</div>
      </div>
    </div>
  );
};

export default function MagiMatrices({ data }) {
  if (!data) return null;
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
      <MatrixCard 
        name="Melchior-1" 
        title="The Scientist" 
        data={data.melchior} 
        colorName="blue"
      />
      <MatrixCard 
        name="Balthasar-2" 
        title="The Mother" 
        data={data.balthasar} 
        colorName="yellow"
      />
      <MatrixCard 
        name="Caspar-3" 
        title="The Woman" 
        data={data.caspar} 
        colorName="orange"
      />
    </div>
  );
}
