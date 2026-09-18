import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:convert';
import '../core/api_client.dart';

import 'student_qr_scanner.dart';

class StudentFaceVerification extends StatefulWidget {
  const StudentFaceVerification({super.key});

  @override
  State<StudentFaceVerification> createState() => _StudentFaceVerificationState();
}

class _StudentFaceVerificationState extends State<StudentFaceVerification> {
  CameraController? _controller;
  List<CameraDescription> _cameras = [];
  bool _isInitializing = true;
  bool _isProcessing = false;
  XFile? _capturedImage;

  @override
  void initState() {
    super.initState();
    _initializeCamera();
  }

  Future<void> _initializeCamera() async {
    try {
      _cameras = await availableCameras();
      if (_cameras.isEmpty) {
        if (mounted) setState(() => _isInitializing = false);
        return;
      }
      
      final frontCamera = _cameras.firstWhere(
        (c) => c.lensDirection == CameraLensDirection.front,
        orElse: () => _cameras.first
      );

      _controller = CameraController(
        frontCamera,
        ResolutionPreset.medium,
        enableAudio: false,
      );

      await _controller!.initialize();
    } catch (e) {
      // ignore
    } finally {
      if (mounted) setState(() => _isInitializing = false);
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  Future<void> _captureFace() async {
    if (_controller == null || !_controller!.value.isInitialized) return;
    if (_controller!.value.isTakingPicture) return;

    try {
      final image = await _controller!.takePicture();
      setState(() => _capturedImage = image);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: const Text('Failed to capture image.'), backgroundColor: Theme.of(context).colorScheme.error),
      );
    }
  }

  Future<void> _submitVerification() async {
    if (_capturedImage == null) return;
    
    setState(() => _isProcessing = true);
    
    try {
      final response = await ApiClient.postMultipart(
        '/student/face-verification/verify',
        fileField: 'file',
        filePath: _capturedImage!.path,
      );
      
      if (!mounted) return;

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final proofToken = data['face_proof_token'];
        
        if (!mounted) return;
        if (_controller != null) {
          await _controller!.dispose();
          _controller = null;
        }

        // Face is verified, now navigate to QR scanner to validate location and scan QR
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(
            builder: (_) => StudentQrScanner(faceProofToken: proofToken),
          ),
        );
      } else {
        String err = "Verification failed. Please try again.";
        try { err = jsonDecode(response.body)['detail'] ?? err; } catch (_) {}
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(err), backgroundColor: Theme.of(context).colorScheme.error),
        );
      }

    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: const Text('Network error. Please check your connection.'), backgroundColor: Theme.of(context).colorScheme.error),
      );
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }

  Widget _buildStepper() {
    return Container(
      color: Theme.of(context).colorScheme.surface,
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          _buildStep(1, 'Identity', true),
          _buildLine(false),
          _buildStep(2, 'Location', false),
          _buildLine(false),
          _buildStep(3, 'Session QR', false),
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
    if (_isInitializing) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    if (_controller == null || !_controller!.value.isInitialized) {
      return Scaffold(
        appBar: AppBar(title: const Text('Identity Verification')),
        body: const Center(child: Text('Camera unavailable. Check device permissions.')),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Identity Verification', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      backgroundColor: Colors.black,
      body: Column(
        children: [
          _buildStepper(),
          Expanded(
            child: _capturedImage == null
                ? Stack(
                    children: [
                      Positioned.fill(child: CameraPreview(_controller!)),
                      // Face positioning guide overlay
                      Center(
                        child: Container(
                          width: 250,
                          height: 350,
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.white.withValues(alpha: 0.5), width: 3),
                            borderRadius: BorderRadius.circular(150),
                          ),
                        ),
                      ),
                      const Positioned(
                        top: 40,
                        left: 0,
                        right: 0,
                        child: Text(
                          'Position your face inside the frame',
                          textAlign: TextAlign.center,
                          style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold, shadows: [Shadow(blurRadius: 4, color: Colors.black)]),
                        ),
                      ),
                      Align(
                        alignment: Alignment.bottomCenter,
                        child: Padding(
                          padding: const EdgeInsets.only(bottom: 32.0),
                          child: FloatingActionButton(
                            backgroundColor: Theme.of(context).colorScheme.secondary,
                            onPressed: _captureFace,
                            child: const Icon(Icons.camera_alt, size: 32, color: Colors.white),
                          ),
                        ),
                      ),
                    ],
                  )
                : Container(
                    color: Theme.of(context).colorScheme.surface,
                    width: double.infinity,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.check_circle_outline, color: Colors.green, size: 80),
                        const SizedBox(height: 24),
                        Text('Image Captured', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold, color: Theme.of(context).colorScheme.primary)),
                        const SizedBox(height: 48),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          children: [
                            TextButton.icon(
                              onPressed: _isProcessing ? null : () => setState(() => _capturedImage = null),
                              icon: const Icon(Icons.refresh),
                              label: const Text('Retake'),
                            ),
                            FilledButton.icon(
                              onPressed: _isProcessing ? null : _submitVerification,
                              icon: _isProcessing 
                                  ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) 
                                  : const Icon(Icons.verified_user),
                              label: Text(_isProcessing ? 'Verifying...' : 'Verify Identity'),
                              style: FilledButton.styleFrom(
                                padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                              ),
                            )
                          ],
                        )
                      ],
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}
