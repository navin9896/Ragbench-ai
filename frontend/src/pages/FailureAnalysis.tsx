import { ChevronRight } from 'lucide-react';

const FailureAnalysis = () => {
  const mockFailures = [
    {
      id: 1,
      question: "What is the return policy for electronics?",
      type: "HALLUCINATION",
      expected: "Electronics can be returned within 14 days in original packaging.",
      generated: "Electronics have a 30-day return window.",
      score: 0.4
    },
    {
      id: 2,
      question: "Who is the VP of Engineering?",
      type: "RETRIEVAL_FAILURE",
      expected: "Sarah Jenkins is the VP of Engineering.",
      generated: "I'm sorry, I couldn't find information about the VP of Engineering.",
      score: 0.1
    },
    {
      id: 3,
      question: "How many paid sick days do part-time employees get?",
      type: "GENERATION_FAILURE",
      expected: "Part-time employees get 3 paid sick days per year.",
      generated: "Part-time employees receive pro-rated sick days.",
      score: 0.6
    }
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Failure Analysis</h1>
        <p className="text-slate-400 mt-1">Review and categorize pipeline failures from the latest evaluation.</p>
      </div>

      <div className="bg-card border border-border rounded-xl overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-900/50 border-b border-border">
              <th className="p-4 font-medium text-slate-400">Question</th>
              <th className="p-4 font-medium text-slate-400">Failure Type</th>
              <th className="p-4 font-medium text-slate-400 hidden lg:table-cell">Expected vs Generated</th>
              <th className="p-4 font-medium text-slate-400">Score</th>
              <th className="p-4"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {mockFailures.map(failure => (
              <tr key={failure.id} className="hover:bg-slate-800/30 transition-colors cursor-pointer group">
                <td className="p-4 max-w-xs truncate text-slate-200">
                  {failure.question}
                </td>
                <td className="p-4">
                  <span className={`px-2 py-1 text-xs rounded-full font-medium border ${
                    failure.type === 'HALLUCINATION' 
                      ? 'bg-red-500/10 text-red-400 border-red-500/20' 
                      : failure.type === 'RETRIEVAL_FAILURE'
                      ? 'bg-orange-500/10 text-orange-400 border-orange-500/20'
                      : 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20'
                  }`}>
                    {failure.type.replace('_', ' ')}
                  </span>
                </td>
                <td className="p-4 text-sm text-slate-400 hidden lg:table-cell max-w-md truncate">
                  <span className="text-emerald-400/70 block truncate">Exp: {failure.expected}</span>
                  <span className="text-red-400/70 block truncate mt-1">Gen: {failure.generated}</span>
                </td>
                <td className="p-4 text-slate-300 font-medium">
                  {failure.score.toFixed(2)}
                </td>
                <td className="p-4 text-right">
                  <ChevronRight className="w-5 h-5 text-slate-600 group-hover:text-primary transition-colors" />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FailureAnalysis;
