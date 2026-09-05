import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../core/api_client.dart';
import 'faculty_live_session.dart';

class FacultyDashboard extends StatefulWidget {
  const FacultyDashboard({super.key});

  @override
  State<FacultyDashboard> createState() => _FacultyDashboardState();
}

class _FacultyDashboardState extends State<FacultyDashboard> {
  List<dynamic> _activeSessions = [];
  bool _isLoadingSessions = true;

  @override
  void initState() {
    super.initState();
    _fetchActiveSessions();
  }

  Future<void> _fetchActiveSessions() async {
    setState(() => _isLoadingSessions = true);
    try {
      final response = await ApiClient.get('/admin/attendance-sessions/active');
      if (response.statusCode == 200) {
        setState(() {
          _activeSessions = jsonDecode(response.body);
        });
      }
    } catch (e) {
      // ignore
    } finally {
      if (mounted) setState(() => _isLoadingSessions = false);
    }
  }

  Future<void> _showStartSessionDialog() async {
    List<dynamic> subjects = [];
    List<dynamic> divisions = [];
    
    try {
      final sRes = await ApiClient.get('/academic/subjects');
      final dRes = await ApiClient.get('/academic/divisions');
      if (sRes.statusCode == 200) subjects = jsonDecode(sRes.body);
      if (dRes.statusCode == 200) divisions = jsonDecode(dRes.body);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Failed to load academic metadata.')));
      return;
    }

    if (!mounted) return;

    int? selectedSubject;
    int? selectedDivision;
    final auth = context.read<AuthService>();

    showDialog(
      context: context,
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setDialogState) {
            return AlertDialog(
              title: Text('Start Attendance Session', style: TextStyle(color: Theme.of(context).colorScheme.primary, fontWeight: FontWeight.bold)),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  DropdownButtonFormField<int>(
                    decoration: const InputDecoration(labelText: 'Subject', border: OutlineInputBorder()),
                    items: subjects.map((s) => DropdownMenuItem<int>(
                      value: s['id'], child: Text(s['name']),
                    )).toList(),
                    onChanged: (v) => setDialogState(() => selectedSubject = v),
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<int>(
                    decoration: const InputDecoration(labelText: 'Division', border: OutlineInputBorder()),
                    items: divisions.map((d) => DropdownMenuItem<int>(
                      value: d['id'], child: Text(d['name']),
                    )).toList(),
                    onChanged: (v) => setDialogState(() => selectedDivision = v),
                  ),
                ],
              ),
              actions: [
                TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
                FilledButton(
                  onPressed: () async {
                    if (selectedSubject == null || selectedDivision == null) return;
                    
                    final response = await ApiClient.post('/admin/attendance-sessions', body: {
                      'faculty_id': auth.userProfile?['id'] ?? 1, // fallback
                      'subject_id': selectedSubject,
                      'division_id': selectedDivision,
                    });
                    
                    if (response.statusCode == 200) {
                      Navigator.pop(ctx);
                      _fetchActiveSessions();
                    }
                  }, 
                  child: const Text('Start Session')
                ),
              ],
            );
          }
        );
      }
    );
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthService>();
    final profile = auth.userProfile ?? {};

    return Scaffold(
      appBar: AppBar(
        title: const Text('SecureAttend', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 0.5)),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchActiveSessions,
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () => auth.logout(),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Good Morning, Prof. ${profile["last_name"] ?? ""}'.trim(),
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.primary,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              'Department of Engineering',
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: Colors.grey.shade600,
                    fontWeight: FontWeight.w500,
                  ),
            ),
            const SizedBox(height: 24),

            // Attendance Module Card (Main Focus)
            Card(
              margin: EdgeInsets.zero,
              child: Padding(
                padding: const EdgeInsets.all(20.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.secondary.withOpacity(0.1),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Icon(
                            Icons.co_present_outlined,
                            color: Theme.of(context).colorScheme.secondary,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Text(
                          'Attendance',
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                fontWeight: FontWeight.bold,
                                color: Theme.of(context).colorScheme.primary,
                              ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),
                    SizedBox(
                      width: double.infinity,
                      child: FilledButton.icon(
                        onPressed: _showStartSessionDialog,
                        icon: const Icon(Icons.add_circle_outline),
                        label: const Text('Start New Session'),
                        style: FilledButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          backgroundColor: Theme.of(context).colorScheme.secondary,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            Text(
              'Active Sessions',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.primary,
                  ),
            ),
            const SizedBox(height: 16),
            
            if (_isLoadingSessions)
              const Center(child: Padding(padding: EdgeInsets.all(32), child: CircularProgressIndicator()))
            else if (_activeSessions.isEmpty)
              Card(
                margin: EdgeInsets.zero,
                child: const Padding(
                  padding: EdgeInsets.all(32.0),
                  child: Center(
                    child: Text(
                      'No active sessions found.',
                      style: TextStyle(color: Colors.grey),
                    ),
                  ),
                ),
              )
            else
              ..._activeSessions.map((session) => Card(
                margin: const EdgeInsets.only(bottom: 12),
                elevation: 0,
                shape: RoundedRectangleBorder(
                  side: BorderSide(color: Theme.of(context).colorScheme.secondary.withOpacity(0.3), width: 1),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: Theme.of(context).colorScheme.secondary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Icon(Icons.qr_code, color: Theme.of(context).colorScheme.secondary),
                  ),
                  title: Text(session['subject_name'] ?? 'Unknown Subject', style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text('${session['division_name'] ?? 'Unknown Div'} • Started at ${DateTime.parse(session['start_time']).toLocal().toString().split('.')[0]}'),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => FacultyLiveSession(sessionId: session['id']),
                      ),
                    ).then((_) => _fetchActiveSessions());
                  },
                ),
              )),
          ],
        ),
      ),
    );
  }
}
