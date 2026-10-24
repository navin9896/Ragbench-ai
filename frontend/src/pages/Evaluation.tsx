import { useState } from 'react';
import { Play, Database, Settings } from 'lucide-react';

const Evaluation = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);

  const handleRunEvaluation = () => {
    setIsRunning(true);
    setProgress(0);
    
    // Simulate evaluation run
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 50) {
          clearInterval(interval);
          setTimeout(() => setIsRunning(false), 500);
          return 50;
        }
        return p + 1;
      });
    }, 50);
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Run Evaluation</h1>
        <p className="text-slate-400 mt-1">Execute the evaluation harness against your golden dataset.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-card border border-border p-6 rounded-xl">
          <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-400" /> Dataset Selection
          </h3>
          <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-slate-200 focus:outline-none focus:border-primary">
            <option value="golden-v1">Golden Dataset v1 (50 questions)</option>
            <option value="edge-cases">Edge Cases (15 questions)</option>
          </select>
        </div>

        <div className="bg-card border border-border p-6 rounded-xl">
          <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
            <Settings className="w-5 h-5 text-purple-400" /> Experiment Config
          </h3>
          <select className="w-full bg-slate-900 border border-slate-700 rounded-lg p-3 text-slate-200 focus:outline-none focus:border-primary">
            <option value="baseline">Baseline (Hybrid, chunk=500)</option>
            <option value="vector-only">Vector Only (chunk=300)</option>
          </select>
        </div>
      </div>

      <div className="bg-card border border-border p-8 rounded-xl flex flex-col items-center justify-center text-center">
        {isRunning ? (
          <div className="w-full max-w-md space-y-6">
            <div className="flex justify-between text-sm text-slate-400 mb-2">
              <span>Evaluating...</span>
              <span>{progress} / 50</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-4 overflow-hidden border border-slate-700">
              <div 
                className="bg-primary h-full transition-all duration-300 ease-out relative overflow-hidden"
                style={{ width: `${(progress / 50) * 100}%` }}
              >
                <div className="absolute inset-0 bg-white/20 animate-[shimmer_1s_infinite]" />
              </div>
            </div>
            <p className="text-sm text-slate-400 italic">Processing chunks and running LLM Judge...</p>
          </div>
        ) : (
          <>
            <Play className="w-16 h-16 text-primary mb-6 opacity-80" />
            <h2 className="text-xl font-semibold mb-2">Ready to Evaluate</h2>
            <p className="text-slate-400 max-w-md mb-8">
              This will run all selected questions through the RAG pipeline and measure retrieval, context, and generation quality.
            </p>
            <button 
              onClick={handleRunEvaluation}
              className="px-8 py-3 bg-primary hover:bg-blue-600 text-primary-foreground font-medium rounded-lg transition-colors shadow-lg shadow-primary/20"
            >
              Start Evaluation Run
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default Evaluation;
