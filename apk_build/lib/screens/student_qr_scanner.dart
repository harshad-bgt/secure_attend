import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../core/api_client.dart';

class StudentQrScanner extends StatefulWidget {
  final String faceProofToken;
  
  const StudentQrScanner({super.key, required this.faceProofToken});

  @override
  State<StudentQrScanner> createState() => _StudentQrScannerState();
}

class _StudentQrScannerState extends State<StudentQrScanner> {
  final MobileScannerController _scannerController = MobileScannerController(
    formats: const [BarcodeFormat.qrCode],
  );
  bool _isProcessing = false;

  @override
  void dispose() {
    _scannerController.dispose();
    super.dispose();
  }

  Future<void> _handleQrDetect(BarcodeCapture capture) async {
    if (_isProcessing) return;
    
    final List<Barcode> barcodes = capture.barcodes;
    if (barcodes.isEmpty || barcodes.first.rawValue == null) return;
    
    final qrData = barcodes.first.rawValue!;
    setState(() => _isProcessing = true);
    
    _scannerController.stop();
    
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        content: Row(
          children: [
            CircularProgressIndicator(color: Theme.of(context).colorScheme.secondary),
            const SizedBox(width: 24),
            const Expanded(child: Text("Verifying Session...", style: TextStyle(fontWeight: FontWeight.bold))),
          ],
        ),
      )
    );

    try {
      final response = await ApiClient.post('/student/attendance/mark', body: {
        'qr_token': qrData,
        'face_proof_token': widget.faceProofToken,
      });
      
      if (!mounted) return;
      Navigator.pop(context); // Close loading

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        _showSuccessDialog(data);
      } else {
        String err = "Verification failed. Session QR may be expired.";
        try { err = jsonDecode(response.body)['detail'] ?? err; } catch (_) {}
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(err), backgroundColor: Theme.of(context).colorScheme.error),
        );
        setState(() => _isProcessing = false);
        _scannerController.start();
      }
    } catch (e) {
      if (!mounted) return;
      Navigator.pop(context);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: const Text('Network error while verifying session.'), backgroundColor: Theme.of(context).colorScheme.error),
      );
      setState(() => _isProcessing = false);
      _scannerController.start();
    }
  }

  void _showSuccessDialog(Map<String, dynamic> data) {
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: Text('Attendance Recorded', style: TextStyle(color: Theme.of(context).colorScheme.primary, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.check_circle, color: Colors.green, size: 80),
            const SizedBox(height: 24),
            _buildChecklistItem('Identity Verified'),
            const SizedBox(height: 8),
            _buildChecklistItem('Session Verified'),
            const SizedBox(height: 8),
            _buildChecklistItem('Attendance Recorded'),
            const SizedBox(height: 24),
            Text(
              '${data["subject_name"]} • ${data["faculty_name"]}',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey.shade700, fontWeight: FontWeight.w500),
            ),
          ],
        ),
        actions: [
          SizedBox(
            width: double.infinity,
            child: FilledButton(
              style: FilledButton.styleFrom(backgroundColor: Theme.of(context).colorScheme.secondary),
              onPressed: () {
                Navigator.pop(ctx);
                Navigator.pop(context); // Go back to dashboard
              }, 
              child: const Text('Return to Dashboard')
            ),
          )
        ],
      )
    );
  }

  Widget _buildChecklistItem(String text) {
    return Row(
      children: [
        const Icon(Icons.check, color: Colors.green, size: 20),
        const SizedBox(width: 8),
        Text(text, style: const TextStyle(fontWeight: FontWeight.bold)),
      ],
    );
  }

  Widget _buildStepper() {
    return Container(
      color: Theme.of(context).colorScheme.surface,
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _buildStep(1, 'Identity', true, isCompleted: true),
          _buildLine(true),
          _buildStep(2, 'Session', true),
          _buildLine(false),
          _buildStep(3, 'Done', false),
        ],
      ),
    );
  }

  Widget _buildStep(int step, String label, bool isActive, {bool isCompleted = false}) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 32,
          height: 32,
          decoration: BoxDecoration(
            color: isActive ? Theme.of(context).colorScheme.primary : Colors.grey.shade300,
            shape: BoxShape.circle,
          ),
          child: Center(
            child: isCompleted 
                ? const Icon(Icons.check, color: Colors.white, size: 18)
                : Text(
                    '$step',
                    style: TextStyle(
                      color: isActive ? Colors.white : Colors.grey.shade600,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            color: isActive ? Theme.of(context).colorScheme.primary : Colors.grey.shade600,
            fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
          ),
        ),
      ],
    );
  }

  Widget _buildLine(bool isActive) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 8).copyWith(bottom: 16),
      width: 40,
      height: 2,
      color: isActive ? Theme.of(context).colorScheme.primary : Colors.grey.shade300,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Scan Attendance QR', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      body: Column(
        children: [
          _buildStepper(),
          Expanded(
            child: Stack(
              children: [
                MobileScanner(
                  controller: _scannerController,
                  onDetect: _handleQrDetect,
                ),
                SafeArea(
                  child: Align(
                    alignment: Alignment.bottomCenter,
                    child: Container(
                      margin: const EdgeInsets.only(bottom: 32),
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primary.withOpacity(0.85),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: const Text(
                        'Point camera at the session QR code',
                        style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
                // Center reticle
                Center(
                  child: Container(
                    width: 250,
                    height: 250,
                    decoration: BoxDecoration(
                      border: Border.all(color: Colors.white.withOpacity(0.5), width: 3),
                      borderRadius: BorderRadius.circular(24),
                    ),
                  ),
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
