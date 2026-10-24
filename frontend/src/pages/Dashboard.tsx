import { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer
} from 'recharts';
import { Activity, CheckCircle, XCircle, Clock } from 'lucide-react';

const Dashboard = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from /api/dashboard/summary
    setTimeout(() => {
      setData({
        metrics: {
          faithfulness: 0.94,
          answer_relevance: 0.93,
          correctness: 0.92,
          recall_at_5: 0.91,
          precision_at_5: 0.87,
          mrr: 0.86,
          failure_rate: 0.08,
          average_latency_ms: 1720
        },
        status: "success",
        latest_run_id: "run-mock-123"
      });
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center h-full text-slate-400">Loading dashboard...</div>;
  }

  if (!data || data.status === 'no_runs') {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-400">
        <Activity className="w-16 h-16 mb-4 opacity-50" />
        <h2 className="text-xl font-semibold text-slate-200">No Evaluation Runs Found</h2>
        <p className="mt-2 text-center max-w-md">Run an evaluation experiment to see metrics here.</p>
      </div>
    );
  }

  const metrics = data.metrics;

  const MetricCard = ({ title, value, icon: Icon, colorClass, suffix = "" }: any) => (
    <div className="bg-card border border-border p-5 rounded-xl shadow-sm hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-sm font-medium text-slate-400">{title}</p>
          <h3 className="text-3xl font-bold mt-2 text-slate-100">
            {typeof value === 'number' && suffix === '%' ? (value * 100).toFixed(1) : value}
            <span className="text-lg ml-1 text-slate-500 font-normal">{suffix}</span>
          </h3>
        </div>
        <div className={`p-3 rounded-lg bg-opacity-10 ${colorClass}`}>
          <Icon className={`w-6 h-6 ${colorClass.replace('bg-', 'text-')}`} />
        </div>
      </div>
    </div>
  );

  const chartData = [
    { name: 'Recall@5', score: metrics.recall_at_5 * 100 },
    { name: 'Precision@5', score: metrics.precision_at_5 * 100 },
    { name: 'MRR', score: metrics.mrr * 100 },
    { name: 'Faithfulness', score: metrics.faithfulness * 100 },
    { name: 'Relevance', score: metrics.answer_relevance * 100 },
    { name: 'Correctness', score: metrics.correctness * 100 },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Platform Overview</h1>
        <p className="text-slate-400 mt-1">Latest evaluation metrics and system health.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard 
          title="Faithfulness" 
          value={metrics.faithfulness} 
          suffix="%"
          icon={CheckCircle} 
          colorClass="bg-emerald-500/20 text-emerald-400" 
        />
        <MetricCard 
          title="Answer Relevance" 
          value={metrics.answer_relevance} 
          suffix="%"
          icon={Activity} 
          colorClass="bg-blue-500/20 text-blue-400" 
        />
        <MetricCard 
          title="Failure Rate" 
          value={metrics.failure_rate} 
          suffix="%"
          icon={XCircle} 
          colorClass="bg-red-500/20 text-red-400" 
        />
        <MetricCard 
          title="Avg Latency" 
          value={(metrics.average_latency_ms / 1000).toFixed(2)} 
          suffix="s"
          icon={Clock} 
          colorClass="bg-purple-500/20 text-purple-400" 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card border border-border p-6 rounded-xl">
          <h3 className="text-lg font-medium mb-6">Quality Metrics Breakdown</h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} domain={[0, 100]} />
                <RechartsTooltip 
                  cursor={{fill: '#1e293b'}} 
                  contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '8px'}}
                  itemStyle={{color: '#60a5fa'}}
                />
                <Bar dataKey="score" fill="#60a5fa" radius={[4, 4, 0, 0]} maxBarSize={50} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-card border border-border p-6 rounded-xl flex flex-col justify-center items-center text-center">
          <h3 className="text-lg font-medium w-full text-left mb-6">System Health</h3>
          <div className="relative w-48 h-48 rounded-full border-8 border-emerald-500/20 flex items-center justify-center before:absolute before:inset-0 before:rounded-full before:border-8 before:border-emerald-500 before:border-t-transparent before:rotate-45">
             <div className="text-center">
               <span className="text-4xl font-bold text-emerald-400">92%</span>
               <p className="text-sm text-slate-400 mt-1">Overall Health</p>
             </div>
          </div>
          <p className="mt-8 text-sm text-slate-400">
            System is performing well above regression thresholds.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
