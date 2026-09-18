import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:geolocator/geolocator.dart';
import 'dart:convert';
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
  bool _isFetchingLocation = true;
  String _statusMessage = 'Validating Location...';
  Position? _currentPosition;

  @override
  void initState() {
    super.initState();
    _fetchLocationAndInit();
  }

  Future<void> _fetchLocationAndInit() async {
    try {
      Position position = await _determinePosition();
      
      if (position.isMocked) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: const Text('Mock location detected. Attendance rejected.'), backgroundColor: Theme.of(context).colorScheme.error),
        );
        setState(() {
          _isFetchingLocation = false;
          _statusMessage = 'Location rejected. Try again.';
        });
        return;
      }
      
      if (!mounted) return;
      
      setState(() {
        _currentPosition = position;
        _isFetchingLocation = false;
        _statusMessage = 'Point camera at the session QR code';
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString()), backgroundColor: Theme.of(context).colorScheme.error),
      );
      setState(() {
        _isFetchingLocation = false;
        _statusMessage = 'Location failed. Please try again.';
      });
    }
  }

  @override
  void dispose() {
    _scannerController.dispose();
    super.dispose();
  }

  Future<void> _handleQrDetect(BarcodeCapture capture) async {
    if (_isProcessing || _currentPosition == null) return;
    
    final List<Barcode> barcodes = capture.barcodes;
    if (barcodes.isEmpty || barcodes.first.rawValue == null) return;
    
    final qrData = barcodes.first.rawValue!;
    setState(() {
      _isProcessing = true;
      _statusMessage = 'Recording attendance...';
    });
    
    _scannerController.stop();

    try {
      final markResponse = await ApiClient.post('/student/attendance/mark', body: {
        'qr_token': qrData,
        'face_proof_token': widget.faceProofToken,
        'latitude': _currentPosition!.latitude,
        'longitude': _currentPosition!.longitude,
      });
      
      if (!mounted) return;

      if (markResponse.statusCode == 200) {
        final markData = jsonDecode(markResponse.body);
        _showSuccessDialog(markData);
      } else {
        String err = "Attendance failed. Session QR may be expired.";
        try { err = jsonDecode(markResponse.body)['detail'] ?? err; } catch (_) {}
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(err), backgroundColor: Theme.of(context).colorScheme.error),
        );
        setState(() {
          _isProcessing = false;
          _statusMessage = 'Scan failed. Try again.';
        });
        _scannerController.start();
      }
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: const Text('Network error. Please check your connection.'), backgroundColor: Theme.of(context).colorScheme.error),
      );
      setState(() {
        _isProcessing = false;
        _statusMessage = 'Network error. Try again.';
      });
      _scannerController.start();
    }
  }

  Future<Position> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return Future.error('Location services are disabled.');
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return Future.error('Location permissions are denied');
      }
    }
    
    if (permission == LocationPermission.deniedForever) {
      return Future.error('Location permissions are permanently denied, we cannot request permissions.');
    } 

    try {
      return await Geolocator.getCurrentPosition(
        locationSettings: const LocationSettings(
          timeLimit: Duration(seconds: 30)
        )
      );
    } catch (e) {
      // Fallback to last known position if timeout or error
      final lastKnown = await Geolocator.getLastKnownPosition();
      if (lastKnown != null) {
        return lastKnown;
      }
      return Future.error('Location timeout. Could not fetch location.');
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
            _buildChecklistItem('Location Verified'),
            const SizedBox(height: 8),
            _buildChecklistItem('Session Verified'),
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
          _buildStep(2, 'Location', true, isCompleted: !_isFetchingLocation && _currentPosition != null),
          _buildLine(!_isFetchingLocation && _currentPosition != null),
          _buildStep(3, 'Session QR', !_isFetchingLocation && _currentPosition != null),
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
                
                if (_isFetchingLocation || _currentPosition == null)
                  Container(
                    color: Theme.of(context).colorScheme.surface,
                    child: const Center(child: CircularProgressIndicator()),
                  ),
                  
                SafeArea(
                  child: Align(
                    alignment: Alignment.bottomCenter,
                    child: Container(
                      margin: const EdgeInsets.only(bottom: 32),
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                      decoration: BoxDecoration(
                        color: Theme.of(context).colorScheme.primary.withValues(alpha: 0.85),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: _isProcessing || _isFetchingLocation
                        ? Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)),
                              const SizedBox(width: 12),
                              Text(_statusMessage, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold))
                            ]
                          )
                        : Text(
                            _statusMessage,
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                          ),
                    ),
                  ),
                ),
                // Center reticle
                if (!_isFetchingLocation && _currentPosition != null)
                  Center(
                    child: Container(
                      width: 250,
                      height: 250,
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.white.withValues(alpha: 0.5), width: 3),
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
