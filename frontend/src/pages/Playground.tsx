import { useState } from 'react';
import { Send, Search, Clock, Cpu, Server, FileText, Activity } from 'lucide-react';

const Playground = () => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleQuery = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsLoading(true);
    
    // In real app, fetch from backend: /api/query
    // MOCK FOR DEMO
    setTimeout(() => {
      setResult({
        answer: "Based on the internal knowledge base, standard shipping typically takes 3-5 business days. Expedited shipping takes 1-2 business days.",
        latency_ms: 840,
        retrieval_latency_ms: 120,
        generation_latency_ms: 720,
        token_usage: {
          input_tokens: 432,
          output_tokens: 28,
          total_cost: 0.0007
        },
        sources: ["doc-104", "doc-211"],
        retrieved_chunks: [
          {
            metadata: { chunk_id: "c-1", document_id: "doc-104", page: 2 },
            content: "Standard shipping takes 3-5 business days across the continental US."
          },
          {
            metadata: { chunk_id: "c-2", document_id: "doc-211", page: 1 },
            content: "For urgent orders, customers can select expedited shipping for 1-2 business day delivery."
          }
        ],
        retrieval_scores: [0.92, 0.85]
      });
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500 h-[calc(100vh-4rem)] flex flex-col">
      <div className="shrink-0">
        <h1 className="text-3xl font-bold tracking-tight">Query Playground</h1>
        <p className="text-slate-400 mt-1">Test the RAG pipeline end-to-end and inspect intermediate steps.</p>
      </div>

      <div className="bg-card border border-border p-2 rounded-xl shadow-sm flex items-center shrink-0">
        <form onSubmit={handleQuery} className="flex-1 flex items-center">
          <Search className="w-5 h-5 text-slate-400 ml-3" />
          <input
            type="text"
            placeholder="Ask a question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent border-none focus:outline-none focus:ring-0 text-slate-100 placeholder:text-slate-500 px-4 py-3"
          />
          <button 
            type="submit"
            disabled={isLoading || !query.trim()}
            className="bg-primary text-primary-foreground p-3 rounded-lg flex items-center justify-center disabled:opacity-50 hover:bg-blue-600 transition-colors"
          >
            {isLoading ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <Send className="w-5 h-5" />}
          </button>
        </form>
      </div>

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1 min-h-0">
          
          {/* Main Answer Column */}
          <div className="lg:col-span-2 space-y-6 overflow-y-auto pr-2 pb-4">
            <div className="bg-card border border-border p-6 rounded-xl shadow-sm">
              <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
                <Server className="w-5 h-5 text-blue-400" /> Generated Answer
              </h3>
              <div className="p-4 bg-slate-900/50 rounded-lg text-slate-200 leading-relaxed border border-slate-800">
                {result.answer}
              </div>
              
              <div className="mt-6 flex flex-wrap gap-4">
                <div className="flex items-center gap-2 text-sm text-slate-400 bg-slate-900/50 px-3 py-1.5 rounded-full border border-slate-800">
                  <Clock className="w-4 h-4 text-emerald-400" />
                  Latency: {result.latency_ms}ms
                </div>
                <div className="flex items-center gap-2 text-sm text-slate-400 bg-slate-900/50 px-3 py-1.5 rounded-full border border-slate-800">
                  <Cpu className="w-4 h-4 text-purple-400" />
                  Tokens: {result.token_usage.input_tokens + result.token_usage.output_tokens}
                </div>
                <div className="flex items-center gap-2 text-sm text-slate-400 bg-slate-900/50 px-3 py-1.5 rounded-full border border-slate-800">
                  <span className="text-yellow-400 font-medium">$</span>
                  Cost: ${result.token_usage.total_cost.toFixed(4)}
                </div>
              </div>
            </div>
            
            <div className="bg-card border border-border p-6 rounded-xl shadow-sm">
              <h3 className="text-lg font-medium mb-4 flex items-center gap-2">
                <Activity className="w-5 h-5 text-emerald-400" /> On-the-fly Evaluation
              </h3>
              <button className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-sm transition-colors border border-slate-700">
                Evaluate This Answer
              </button>
              <p className="text-xs text-slate-500 mt-3">Click to run the LLM Judge on this specific response pair.</p>
            </div>
          </div>
          
          {/* Context Column */}
          <div className="bg-card border border-border p-6 rounded-xl shadow-sm overflow-y-auto pb-4 flex flex-col">
            <h3 className="text-lg font-medium mb-4 flex items-center gap-2 shrink-0">
              <FileText className="w-5 h-5 text-orange-400" /> Retrieved Context
            </h3>
            
            <div className="space-y-4 flex-1">
              {result.retrieved_chunks.map((chunk: any, i: number) => (
                <div key={i} className="p-4 bg-slate-900/50 rounded-lg border border-slate-800 relative group">
                  <div className="absolute top-3 right-3 text-xs font-medium text-emerald-400 bg-emerald-400/10 px-2 py-0.5 rounded-full border border-emerald-400/20">
                    Score: {result.retrieval_scores[i].toFixed(2)}
                  </div>
                  <h4 className="text-sm font-medium text-slate-300 mb-2 pr-20 truncate">
                    {chunk.metadata.document_id}
                  </h4>
                  <p className="text-sm text-slate-400">
                    {chunk.content}
                  </p>
                </div>
              ))}
            </div>
          </div>
          
        </div>
      )}
    </div>
  );
};

export default Playground;
