import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  Users, 
  FileCheck, 
  Settings, 
  LogOut,
  School,
  Bell
} from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className="bg-gray-900 text-white w-64 min-h-screen p-4 fixed left-0 top-0">
      <div className="flex items-center gap-3 mb-8">
        <School className="w-8 h-8 text-emerald-500" />
        <div>
          <h1 className="font-bold text-lg">Mufakose 2</h1>
          <p className="text-sm text-gray-400">Secondary School</p>
        </div>
      </div>
      
      <nav className="space-y-2">
        <SidebarLink to="/students" icon={<Users />} text="Students" />
        <SidebarLink to="/applications" icon={<FileCheck />} text="Applications" />
        <SidebarLink to="/notifications" icon={<Bell />} text="Notifications" />
        <SidebarLink to="/settings" icon={<Settings />} text="Settings" />
      </nav>
      
      <button className="flex items-center gap-3 text-red-400 hover:text-red-300 transition-colors mt-auto absolute bottom-8 left-4 w-full pr-4">
        <LogOut className="w-5 h-5" />
        <span>Logout</span>
      </button>
    </aside>
  );
}

function SidebarLink({ icon, text, to }: { 
  icon: React.ReactNode; 
  text: string; 
  to: string;
}) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => `
        flex items-center gap-3 px-4 py-3 rounded-lg transition-colors
        ${isActive 
          ? 'bg-emerald-600 text-white' 
          : 'text-gray-400 hover:text-white hover:bg-gray-800'
        }
      `}
    >
      <span className="w-5 h-5">{icon}</span>
      <span>{text}</span>
    </NavLink>
  );
}