import React, { useState, useEffect } from 'react';

const frames = [
  "SYSTEM STARTUP",
  "INITIALIZING MAGI",
  "MELCHIOR-1: ONLINE",
  "BALTHASAR-2: ONLINE",
  "CASPAR-3: ONLINE",
  "SYNC RATIO 400%",
  "EVALUATING...",
  "PLEASE WAIT"
];

export default function TerminalLoader() {
  const [frameIndex, setFrameIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setFrameIndex(prev => (prev + 1) % frames.length);
    }, 120);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center h-64 border-2 border-nerv-orange bg-black mb-8 p-4">
      <div className="text-white px-4 py-2 text-4xl font-serif uppercase tracking-widest font-black flex items-center justify-center">
        <span className="mechanically-compressed-center" style={{ filter: frameIndex % 2 === 0 ? 'invert(1)' : 'none', background: frameIndex % 2 === 0 ? 'black' : 'white' }}>
          {frames[frameIndex]}
        </span>
      </div>
      <div className="mt-4 text-nerv-green font-mono text-sm animate-pulse">
        [ SYSTEM OVERRIDE / SECURE CHANNEL ]
      </div>
    </div>
  );
}
