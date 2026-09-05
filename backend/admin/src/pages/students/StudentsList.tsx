import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { UserPlus, Search, Eye, ShieldAlert, ShieldCheck } from 'lucide-react';
import toast from 'react-hot-toast';

import apiClient from '../../api/client';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../../components/ui/Table';
import { Badge } from '../../components/ui/Badge';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Dialog } from '../../components/ui/Dialog';

export default function StudentsList() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: students = [], isLoading } = useQuery({
    queryKey: ['students'],
    queryFn: async () => {
      const { data } = await apiClient.get('/students/');
      return data;
    }
  });

  const toggleStatusMutation = useMutation({
    mutationFn: async (userId: number) => {
      await apiClient.post(`/students/${userId}/toggle-status`);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
      toast.success('Student status updated successfully');
    },
    onError: () => toast.error('Failed to update status')
  });

  const filteredStudents = students.filter((s: any) => 
    s.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.roll_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Students</h1>
          <p className="text-slate-500 dark:text-slate-400">Manage student accounts and enrollment</p>
        </div>
        <Button onClick={() => setIsCreateOpen(true)} className="flex items-center gap-2">
          <UserPlus size={18} />
          <span>Add Student</span>
        </Button>
      </div>

      <Card>
        <CardHeader className="flex flex-col sm:flex-row justify-between items-center gap-4">
          <CardTitle>All Students</CardTitle>
          <div className="relative w-full sm:w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <Input 
              placeholder="Search by name or roll number..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 h-10"
            />
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="p-8 text-center text-slate-500 dark:text-slate-400">Loading students...</div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Roll Number</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Email</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredStudents.length > 0 ? filteredStudents.map((student: any) => (
                  <TableRow key={student.user_id}>
                    <TableCell className="font-medium text-slate-900 dark:text-white">
                      {student.roll_number}
                    </TableCell>
                    <TableCell>{student.first_name} {student.last_name}</TableCell>
                    <TableCell>{student.email}</TableCell>
                    <TableCell>
                      <Badge variant={student.is_active ? 'success' : 'error'}>
                        {student.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          onClick={() => navigate(`/students/${student.user_id}`)}
                          title="View Details"
                        >
                          <Eye size={18} />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => toggleStatusMutation.mutate(student.user_id)}
                          title={student.is_active ? "Deactivate" : "Activate"}
                          className={student.is_active ? "text-red-500 hover:text-red-600" : "text-green-500 hover:text-green-600"}
                        >
                          {student.is_active ? <ShieldAlert size={18} /> : <ShieldCheck size={18} />}
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                )) : (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-slate-500 dark:text-slate-400">
                      No students found matching your search.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>

      <CreateStudentDialog isOpen={isCreateOpen} onClose={() => setIsCreateOpen(false)} />
    </div>
  );
}

function CreateStudentDialog({ isOpen, onClose }: { isOpen: boolean, onClose: () => void }) {
  const queryClient = useQueryClient();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    roll_number: ''
  });

  const createMutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      await apiClient.post('/students/', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
      toast.success('Student created successfully');
      onClose();
      setFormData({ first_name: '', last_name: '', email: '', password: '', roll_number: '' });
    },
    onError: (err: any) => {
      toast.error(err.response?.data?.detail || 'Failed to create student');
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(formData);
  };

  return (
    <Dialog isOpen={isOpen} onClose={onClose} title="Add New Student">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Input 
            label="First Name" 
            required 
            value={formData.first_name}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({...formData, first_name: e.target.value})}
          />
          <Input 
            label="Last Name" 
            required 
            value={formData.last_name}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({...formData, last_name: e.target.value})}
          />
        </div>
        <Input 
          label="Roll Number" 
          required 
          value={formData.roll_number}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({...formData, roll_number: e.target.value})}
        />
        <Input 
          label="Email Address" 
          type="email" 
          required 
          value={formData.email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({...formData, email: e.target.value})}
        />
        <Input 
          label="Temporary Password" 
          type="password" 
          required 
          value={formData.password}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({...formData, password: e.target.value})}
        />
        <div className="pt-4 flex justify-end gap-3">
          <Button type="button" variant="ghost" onClick={onClose}>Cancel</Button>
          <Button type="submit" isLoading={createMutation.isPending}>Create Student</Button>
        </div>
      </form>
    </Dialog>
  );
}
