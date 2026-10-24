import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, FileSpreadsheet, AlertOctagon, Settings } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Query Playground', path: '/playground', icon: MessageSquare },
    { name: 'Evaluation', path: '/evaluation', icon: FileSpreadsheet },
    { name: 'Failure Analysis', path: '/failures', icon: AlertOctagon },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <div className="w-64 border-r border-border bg-card flex flex-col">
      <div className="p-6">
        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-primary bg-clip-text text-transparent">
          RAGBench AI
        </h1>
        <p className="text-xs text-slate-400 mt-1">Platform v1.0</p>
      </div>
      
      <nav className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item) => (
          <NavLink
            key={item.name}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-md transition-all ${
                isActive 
                  ? 'bg-primary/10 text-primary font-medium border border-primary/20 shadow-[0_0_15px_rgba(59,130,246,0.1)]' 
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
