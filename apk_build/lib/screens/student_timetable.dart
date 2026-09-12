import 'package:flutter/material.dart';
import 'dart:convert';
import '../core/api_client.dart';

class StudentTimetableScreen extends StatefulWidget {
  const StudentTimetableScreen({super.key});

  @override
  State<StudentTimetableScreen> createState() => _StudentTimetableScreenState();
}

class _StudentTimetableScreenState extends State<StudentTimetableScreen> {
  List<dynamic> _timetable = [];
  bool _isLoading = true;
  String? _error;

  final List<String> _days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  @override
  void initState() {
    super.initState();
    _fetchTimetable();
  }

  Future<void> _fetchTimetable() async {
    try {
      final response = await ApiClient.get('/api/v1/erp/timetable/student');
      if (response.statusCode == 200) {
        setState(() {
          _timetable = json.decode(response.body);
          // Sort by day and start time
          _timetable.sort((a, b) {
            int dayDiff = (a['day_of_week'] ?? 0).compareTo(b['day_of_week'] ?? 0);
            if (dayDiff != 0) return dayDiff;
            return (a['start_time'] ?? '').compareTo(b['start_time'] ?? '');
          });
          _isLoading = false;
        });
      } else {
        setState(() {
          _error = 'Failed to load timetable: ${response.statusCode}';
          _isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Network error: $e';
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Timetable'),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(_error!, style: const TextStyle(color: Colors.red)),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _isLoading = true;
                  _error = null;
                });
                _fetchTimetable();
              },
              child: const Text('Retry'),
            ),
          ],
        ),
      );
    }
    if (_timetable.isEmpty) {
      return const Center(child: Text('No timetable found.'));
    }

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: _timetable.length,
      itemBuilder: (context, index) {
        final entry = _timetable[index];
        final dayIndex = (entry['day_of_week'] as int?) ?? 1;
        final dayName = (dayIndex >= 1 && dayIndex <= 7) ? _days[dayIndex - 1] : 'Unknown Day';
        
        return Card(
          margin: const EdgeInsets.only(bottom: 12),
          child: ListTile(
            leading: CircleAvatar(
              backgroundColor: Theme.of(context).colorScheme.primaryContainer,
              child: Text(dayName.substring(0, 3)),
            ),
            title: Text('Subject ID: ${entry['subject_id']}'),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 4),
                Text('$dayName • ${entry['start_time']} - ${entry['end_time']}'),
                if (entry['room'] != null && entry['room'].toString().isNotEmpty)
                  Text('Room: ${entry['room']}'),
              ],
            ),
            isThreeLine: true,
          ),
        );
      },
    );
  }
}
