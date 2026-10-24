import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Playground from './pages/Playground';
import Evaluation from './pages/Evaluation';
import FailureAnalysis from './pages/FailureAnalysis';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-background text-foreground overflow-hidden font-sans">
        <Sidebar />
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-6xl mx-auto">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/playground" element={<Playground />} />
              <Route path="/evaluation" element={<Evaluation />} />
              <Route path="/failures" element={<FailureAnalysis />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </div>
        </main>
      </div>
    </Router>
  )
}

export default App
