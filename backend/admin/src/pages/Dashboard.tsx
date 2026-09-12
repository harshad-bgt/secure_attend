import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Users, BookOpen, Clock, BarChart3, ShieldCheck, GraduationCap, Building2, ClipboardList } from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<string>('overview');

  if (!user) return null;

  const isAdmin = user.role === 'ADMIN';
  const isFaculty = user.role === 'FACULTY' || isAdmin;
  const isHOD = user.responsibilities?.is_hod || isAdmin;
  const isAMC = user.responsibilities?.is_amc || isAdmin;
  const isGFM = user.responsibilities?.is_gfm || isAdmin;

  const tabs = [];
  
  if (isFaculty) {
    tabs.push({ id: 'overview', label: 'Faculty Portal', icon: BookOpen });
  }
  if (isGFM) {
    tabs.push({ id: 'gfm', label: 'GFM Dashboard', icon: Users });
  }
  if (isAMC) {
    tabs.push({ id: 'amc', label: 'AMC Console', icon: Clock });
  }
  if (isHOD) {
    tabs.push({ id: 'hod', label: 'HOD Analytics', icon: BarChart3 });
  }
  if (isAdmin) {
    tabs.push({ id: 'admin', label: 'Admin Settings', icon: ShieldCheck });
  }

  // Fallback to overview if tab becomes invalid
  if (!tabs.find(t => t.id === activeTab) && tabs.length > 0) {
    setActiveTab(tabs[0].id);
  }

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-950 p-6 rounded-xl border dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
            Welcome back, {user.first_name || 'User'}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            Access level: <span className="font-semibold text-blue-600 dark:text-blue-400">{user.role}</span>
            {user.responsibilities?.is_hod && <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300">HOD</span>}
            {user.responsibilities?.is_amc && <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300">AMC</span>}
            {user.responsibilities?.is_gfm && <span className="ml-2 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300">GFM</span>}
          </p>
        </div>
      </div>

      {/* Tabs Navigation */}
      <div className="border-b border-slate-200 dark:border-slate-800">
        <nav className="-mb-px flex space-x-8 overflow-x-auto" aria-label="Tabs">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={
                  `whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors ${isActive ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300 dark:text-slate-400 dark:hover:text-slate-300 dark:hover:border-slate-600'}`
                }
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-blue-500' : 'text-slate-400 group-hover:text-slate-500'}`} />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Tab Content Panels */}
      <div className="mt-6">
        {activeTab === 'overview' && isFaculty && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <DashboardCard title="My Subjects" icon={BookOpen} value="4" desc="Assigned this semester" />
            <DashboardCard title="Pending Approvals" icon={ClipboardList} value="2" desc="Leave & corrections" />
          </div>
        )}
        
        {activeTab === 'gfm' && isGFM && (
          <div className="bg-white dark:bg-slate-950 p-6 rounded-xl border dark:border-slate-800 shadow-sm">
            <h3 className="text-lg font-bold mb-4 text-slate-800 dark:text-slate-100">GFM Student List</h3>
            <p className="text-slate-500 text-sm">Monitor attendance, results, and mentoring for your assigned SE students.</p>
          </div>
        )}

        {activeTab === 'amc' && isAMC && (
          <div className="bg-white dark:bg-slate-950 p-6 rounded-xl border dark:border-slate-800 shadow-sm">
            <h3 className="text-lg font-bold mb-4 text-slate-800 dark:text-slate-100">Academic Monitoring</h3>
            <p className="text-slate-500 text-sm">Manage timetable schedules, official results publishing, and curriculum coverage.</p>
          </div>
        )}

        {activeTab === 'hod' && isHOD && (
          <div className="bg-white dark:bg-slate-950 p-6 rounded-xl border dark:border-slate-800 shadow-sm">
            <h3 className="text-lg font-bold mb-4 text-slate-800 dark:text-slate-100">Department Overview</h3>
            <p className="text-slate-500 text-sm">Approve faculty leaves, review department-wide analytics, and assign HOD/AMC roles.</p>
          </div>
        )}

        {activeTab === 'admin' && isAdmin && (
          <div className="bg-white dark:bg-slate-950 p-6 rounded-xl border dark:border-slate-800 shadow-sm">
            <h3 className="text-lg font-bold mb-4 text-slate-800 dark:text-slate-100">System Administration</h3>
            <p className="text-slate-500 text-sm">Manage global settings, user accounts, and system-wide configurations.</p>
          </div>
        )}
      </div>
    </div>
  );
}

function DashboardCard({ title, icon: Icon, value, desc }: { title: string, icon: any, value: string, desc: string }) {
  return (
    <div className="bg-white dark:bg-slate-950 p-6 rounded-xl border dark:border-slate-800 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center gap-4">
        <div className="p-3 bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 rounded-lg">
          <Icon className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</h3>
          <p className="text-2xl font-bold text-slate-800 dark:text-slate-100">{value}</p>
        </div>
      </div>
      <p className="mt-4 text-sm text-slate-600 dark:text-slate-400">{desc}</p>
    </div>
  );
}
