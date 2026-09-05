import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Users, BookOpen, Clock, BarChart3, ShieldCheck, GraduationCap, Building2, ClipboardList } from 'lucide-react';

export default function Dashboard() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-slate-950 p-6 rounded-xl border dark:border-slate-800 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
            Welcome back, {user.first_name || 'User'}
          </h2>
          <p className="text-slate-600 dark:text-slate-400 mt-1">
            Access level: <span className="font-semibold text-blue-600 dark:text-blue-400">{user.role}</span>
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <DashboardCard title="Active Students" icon={Users} value="--" desc="Enrolled in system" />
        <DashboardCard title="Active Sessions" icon={Clock} value="--" desc="Ongoing currently" />
        <DashboardCard title="Pending Approvals" icon={ClipboardList} value="--" desc="Requires review" />
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
