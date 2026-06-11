import React from 'react';

export default function MagiInfo() {
  return (
    <div className="mb-10 border border-gray-800 bg-[#0c0c0e] p-6 md:p-8 text-gray-300 font-sans flex flex-col md:flex-row gap-8 items-start relative overflow-hidden">
      {/* Decorative background logo */}
      <div className="absolute -right-10 -bottom-10 opacity-[0.02] pointer-events-none">
        <div className="text-[150px] font-serif mechanically-compressed font-black">NERV</div>
      </div>

      <div className="md:w-1/3 border-l-4 border-nerv-red pl-6 relative z-10">
        <h2 className="text-white font-mono text-3xl font-black uppercase mechanically-compressed tracking-tight  mb-3">
          MAGI System [Tokyo-3]
        </h2>
        <p className="text-sm leading-relaxed text-gray-400">
          The biological supercomputer architecture governing NERV's decisions. 
          Its foundation utilizes a personality-transplant OS modeled after its creator, Dr. Naoko Akagi. 
          All final decisions require a unanimous consensus among its three independent cores.
        </p>
      </div>
      <div className="md:w-2/3 grid grid-cols-1 sm:grid-cols-3 gap-6 relative z-10 w-full">
        <div className="border border-blue-500/30 bg-blue-500/5 p-4 flex flex-col">
          <div className="font-bold text-blue-500 text-xs tracking-widest uppercase mb-2">Melchior-1</div>
          <div className="text-sm text-gray-400 leading-relaxed">
            Modeled on her persona as a <strong className="text-white">Scientist</strong>. Prioritizes raw data and logic.
          </div>
        </div>
        <div className="border border-yellow-500/30 bg-yellow-500/5 p-4 flex flex-col">
          <div className="font-bold text-yellow-500 text-xs tracking-widest uppercase mb-2">Balthasar-2</div>
          <div className="text-sm text-gray-400 leading-relaxed">
            Modeled on her persona as a <strong className="text-white">Mother</strong>. Prioritizes empathy and morality.
          </div>
        </div>
        <div className="border border-nerv-orange/30 bg-nerv-orange/5 p-4 flex flex-col">
          <div className="font-bold text-nerv-orange text-xs tracking-widest uppercase mb-2">Caspar-3</div>
          <div className="text-sm text-gray-400 leading-relaxed">
            Modeled on her persona as a <strong className="text-white">Woman</strong>. Prioritizes speed, pragmatism, and emotion.
          </div>
        </div>
      </div>
    </div>
  );
}
