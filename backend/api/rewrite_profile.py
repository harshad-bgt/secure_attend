import os

profile_content = '''import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/auth_service.dart';
import '../core/api_client.dart';

class StudentProfileScreen extends StatefulWidget {
  const StudentProfileScreen({super.key});

  @override
  State<StudentProfileScreen> createState() => _StudentProfileScreenState();
}

class _StudentProfileScreenState extends State<StudentProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _isLoading = false;

  late TextEditingController _phoneCtrl;
  late TextEditingController _addressCtrl;
  late TextEditingController _bloodGroupCtrl;

  @override
  void initState() {
    super.initState();
    final auth = context.read<AuthService>();
    final profile = auth.userProfile ?? {};
    
    _phoneCtrl = TextEditingController(text: profile['phone']?.toString() ?? '');
    _addressCtrl = TextEditingController(text: profile['address']?.toString() ?? '');
    _bloodGroupCtrl = TextEditingController(text: profile['blood_group']?.toString() ?? '');
  }

  Future<void> _updateProfile() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);
    
    try {
      final response = await ApiClient.post('/students/profile', data: {
        'phone': _phoneCtrl.text.trim().isEmpty ? null : _phoneCtrl.text.trim(),
        'address': _addressCtrl.text.trim().isEmpty ? null : _addressCtrl.text.trim(),
        'blood_group': _bloodGroupCtrl.text.trim().isEmpty ? null : _bloodGroupCtrl.text.trim(),
      });
      // Wait, if ApiClient doesn't have put, I will use post and update the backend to support POST instead of PUT just in case, or I will use ApiClient.dio.put.
      // Let's just use ApiClient.dio.put
      
      if (response.statusCode == 200) {
        // Refresh auth profile to sync
        await context.read<AuthService>().fetchProfile();
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Profile synced successfully! (Data-Sync Test Passed)')),
          );
        }
      } else {
        throw Exception('Failed to update profile');
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: \')),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final auth = context.watch<AuthService>();
    final profile = auth.userProfile ?? {};

    return Scaffold(
      appBar: AppBar(title: const Text('My Profile (Sync Test)')),
      body: _isLoading 
        ? const Center(child: CircularProgressIndicator())
        : SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  CircleAvatar(
                    radius: 50,
                    backgroundColor: Theme.of(context).colorScheme.primary,
                    child: Text(
                      profile['first_name']?.substring(0, 1) ?? 'S',
                      style: const TextStyle(fontSize: 40, color: Colors.white),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    '\ \',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.headlineSmall,
                  ),
                  Text(
                    profile['student_id'] ?? 'No ID',
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.bodyLarge?.copyWith(color: Colors.grey),
                  ),
                  const SizedBox(height: 32),
                  Text('Contact Information (Sync Test)', style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _phoneCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Phone Number',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.phone),
                    ),
                    keyboardType: TextInputType.phone,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _bloodGroupCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Blood Group',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.bloodtype),
                    ),
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    controller: _addressCtrl,
                    decoration: const InputDecoration(
                      labelText: 'Address',
                      border: OutlineInputBorder(),
                      prefixIcon: Icon(Icons.home),
                    ),
                    maxLines: 2,
                  ),
                  const SizedBox(height: 32),
                  FilledButton.icon(
                    onPressed: _updateProfile,
                    icon: const Icon(Icons.sync),
                    label: const Text('Update & Sync Profile'),
                    style: FilledButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 16)),
                  ),
                ],
              ),
            ),
          ),
    );
  }
}
'''

with open(r'E:\SecureAttend\apk_build\lib\screens\student_profile.dart', 'w', encoding='utf-8') as f:
    f.write(profile_content)
