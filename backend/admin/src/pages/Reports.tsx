import { BarChart3, PieChart, Users, BookOpen } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export default function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Attendance Reports</h1>
        <p className="text-slate-500 dark:text-slate-400">View analytics and export attendance data</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <ReportTypeCard 
          title="Student-wise" 
          description="Detailed attendance percentage for individual students across all subjects."
          icon={Users}
        />
        <ReportTypeCard 
          title="Subject-wise" 
          description="Aggregated attendance statistics for specific academic subjects."
          icon={BookOpen}
        />
        <ReportTypeCard 
          title="Faculty-wise" 
          description="Overview of sessions conducted by faculty members."
          icon={PieChart}
        />
        <ReportTypeCard 
          title="Division-wise" 
          description="Aggregate statistics for entire divisions and classrooms."
          icon={BarChart3}
        />
      </div>

      <Card className="mt-8 bg-slate-50 border-dashed dark:bg-slate-900/50">
        <CardContent className="flex flex-col items-center justify-center py-16 text-center">
          <BarChart3 size={48} className="text-slate-300 dark:text-slate-600 mb-4" />
          <h2 className="text-xl font-bold text-slate-700 dark:text-slate-300 mb-2">Advanced Reporting Coming Soon</h2>
          <p className="text-slate-500 dark:text-slate-400 max-w-md mb-6">
            Detailed CSV/PDF exports and complex multi-parameter filtering are planned for a future update once backend analytical endpoints are fully implemented.
          </p>
          <div className="flex gap-4">
            <Button disabled variant="outline">Export CSV (Disabled)</Button>
            <Button disabled>Generate PDF (Disabled)</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

function ReportTypeCard({ title, description, icon: Icon }: any) {
  return (
    <Card className="hover:border-blue-300 transition-colors">
      <CardHeader className="pb-2">
        <Icon className="text-blue-500 mb-2" size={24} />
        <CardTitle className="text-lg">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-slate-500 dark:text-slate-400">{description}</p>
        <Button variant="ghost" size="sm" className="w-full mt-4" disabled>
          View Report
        </Button>
      </CardContent>
    </Card>
  );
}
