import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Building2, BookOpen, Users, Plus } from 'lucide-react';
import toast from 'react-hot-toast';

import apiClient from '../../api/client';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../../components/ui/Table';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Dialog } from '../../components/ui/Dialog';

export default function AcademicOverview() {
  const [activeTab, setActiveTab] = useState<'departments' | 'subjects' | 'divisions'>('departments');

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Academic Management</h1>
        <p className="text-slate-500 dark:text-slate-400">Manage departments, subjects, and academic structure</p>
      </div>

      <div className="flex border-b border-slate-200 dark:border-slate-800">
        <button
          className={`flex items-center space-x-2 px-6 py-3 font-medium transition-colors border-b-2 ${
            activeTab === 'departments' 
              ? 'border-blue-600 text-blue-600 dark:text-blue-500' 
              : 'border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200'
          }`}
          onClick={() => setActiveTab('departments')}
        >
          <Building2 size={18} />
          <span>Departments</span>
        </button>
        <button
          className={`flex items-center space-x-2 px-6 py-3 font-medium transition-colors border-b-2 ${
            activeTab === 'subjects' 
              ? 'border-blue-600 text-blue-600 dark:text-blue-500' 
              : 'border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200'
          }`}
          onClick={() => setActiveTab('subjects')}
        >
          <BookOpen size={18} />
          <span>Subjects</span>
        </button>
        <button
          className={`flex items-center space-x-2 px-6 py-3 font-medium transition-colors border-b-2 ${
            activeTab === 'divisions' 
              ? 'border-blue-600 text-blue-600 dark:text-blue-500' 
              : 'border-transparent text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200'
          }`}
          onClick={() => setActiveTab('divisions')}
        >
          <Users size={18} />
          <span>Divisions</span>
        </button>
      </div>

      {activeTab === 'departments' ? <DepartmentsTab /> : activeTab === 'subjects' ? <SubjectsTab /> : <DivisionsTab />}
    </div>
  );
}

function DepartmentsTab() {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({ code: '', name: '' });
  const queryClient = useQueryClient();

  const { data: departments = [], isLoading } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const { data } = await apiClient.get('/academic/departments');
      return data;
    }
  });

  const createMutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      await apiClient.post('/academic/departments', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['departments'] });
      toast.success('Department added successfully');
      setIsOpen(false);
      setFormData({ code: '', name: '' });
    },
    onError: () => toast.error('Failed to add department')
  });

  return (
    <Card>
      <CardHeader className="flex flex-row justify-between items-center">
        <CardTitle>Departments</CardTitle>
        <Button onClick={() => setIsOpen(true)} size="sm" className="flex items-center gap-1">
          <Plus size={16} /> Add Department
        </Button>
      </CardHeader>
      <CardContent className="p-0">
        {isLoading ? (
          <div className="p-8 text-center text-slate-500">Loading...</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Code</TableHead>
                <TableHead>Department Name</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {departments.length > 0 ? departments.map((d: any) => (
                <TableRow key={d.id}>
                  <TableCell className="font-medium">{d.code}</TableCell>
                  <TableCell>{d.name}</TableCell>
                </TableRow>
              )) : (
                <TableRow>
                  <TableCell colSpan={2} className="text-center py-6 text-slate-500">No departments found.</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        )}
      </CardContent>

      <Dialog isOpen={isOpen} onClose={() => setIsOpen(false)} title="Add Department">
        <form onSubmit={(e: React.FormEvent) => { e.preventDefault(); createMutation.mutate(formData); }} className="space-y-4">
          <Input 
            label="Department Code" 
            placeholder="e.g. CS"
            required 
            value={formData.code}
            onChange={(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setFormData({...formData, code: e.target.value})}
          />
          <Input 
            label="Department Name" 
            placeholder="e.g. Computer Science"
            required 
            value={formData.name}
            onChange={(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setFormData({...formData, name: e.target.value})}
          />
          <div className="pt-4 flex justify-end gap-3">
            <Button type="button" variant="ghost" onClick={() => setIsOpen(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Save</Button>
          </div>
        </form>
      </Dialog>
    </Card>
  );
}

function SubjectsTab() {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({ code: '', name: '', department_id: '' });
  const queryClient = useQueryClient();

  const { data: subjects = [], isLoading } = useQuery({
    queryKey: ['subjects'],
    queryFn: async () => {
      const { data } = await apiClient.get('/academic/subjects');
      return data;
    }
  });

  const { data: departments = [] } = useQuery({
    queryKey: ['departments'],
    queryFn: async () => {
      const { data } = await apiClient.get('/academic/departments');
      return data;
    }
  });

  const createMutation = useMutation({
    mutationFn: async (data: any) => {
      await apiClient.post('/academic/subjects', {
        ...data,
        department_id: parseInt(data.department_id)
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['subjects'] });
      toast.success('Subject added successfully');
      setIsOpen(false);
      setFormData({ code: '', name: '', department_id: '' });
    },
    onError: () => toast.error('Failed to add subject')
  });

  return (
    <Card>
      <CardHeader className="flex flex-row justify-between items-center">
        <CardTitle>Subjects</CardTitle>
        <Button onClick={() => setIsOpen(true)} size="sm" className="flex items-center gap-1">
          <Plus size={16} /> Add Subject
        </Button>
      </CardHeader>
      <CardContent className="p-0">
        {isLoading ? (
          <div className="p-8 text-center text-slate-500">Loading...</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Code</TableHead>
                <TableHead>Subject Name</TableHead>
                <TableHead>Department ID</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {subjects.length > 0 ? subjects.map((s: any) => (
                <TableRow key={s.id}>
                  <TableCell className="font-medium">{s.code}</TableCell>
                  <TableCell>{s.name}</TableCell>
                  <TableCell>{s.department_id}</TableCell>
                </TableRow>
              )) : (
                <TableRow>
                  <TableCell colSpan={3} className="text-center py-6 text-slate-500">No subjects found.</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        )}
      </CardContent>

      <Dialog isOpen={isOpen} onClose={() => setIsOpen(false)} title="Add Subject">
        <form onSubmit={(e: React.FormEvent) => { e.preventDefault(); createMutation.mutate(formData); }} className="space-y-4">
          <Input 
            label="Subject Code" 
            placeholder="e.g. CS101"
            required 
            value={formData.code}
            onChange={(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setFormData({...formData, code: e.target.value})}
          />
          <Input 
            label="Subject Name" 
            placeholder="e.g. Intro to Programming"
            required 
            value={formData.name}
            onChange={(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setFormData({...formData, name: e.target.value})}
          />
          <div className="w-full">
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">
              Department
            </label>
            <select
              required
              value={formData.department_id}
              onChange={(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setFormData({...formData, department_id: e.target.value})}
              className="w-full px-4 py-2 rounded-lg border border-slate-300 focus:border-blue-500 bg-white dark:bg-slate-900 text-slate-900 dark:text-white dark:border-slate-700"
            >
              <option value="" disabled>Select Department</option>
              {departments.map((d: any) => (
                <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
              ))}
            </select>
          </div>
          <div className="pt-4 flex justify-end gap-3">
            <Button type="button" variant="ghost" onClick={() => setIsOpen(false)}>Cancel</Button>
            <Button type="submit" isLoading={createMutation.isPending}>Save</Button>
          </div>
        </form>
      </Dialog>
    </Card>
  );
}

function DivisionsTab() {
  const { data: divisions = [], isLoading } = useQuery({
    queryKey: ['divisions'],
    queryFn: async () => {
      const { data } = await apiClient.get('/academic/divisions');
      return data;
    }
  });

  return (
    <Card>
      <CardHeader className="flex flex-row justify-between items-center">
        <CardTitle>Divisions</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        {isLoading ? (
          <div className="p-8 text-center text-slate-500">Loading...</div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Division Name</TableHead>
                <TableHead>Semester ID</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {divisions.length > 0 ? divisions.map((d: any) => (
                <TableRow key={d.id}>
                  <TableCell className="font-medium">{d.name}</TableCell>
                  <TableCell>{d.semester_id}</TableCell>
                </TableRow>
              )) : (
                <TableRow>
                  <TableCell colSpan={2} className="text-center py-6 text-slate-500">No divisions found.</TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
