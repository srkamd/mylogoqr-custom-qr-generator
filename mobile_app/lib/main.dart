import 'dart:convert';
import 'dart:io';
import 'dart:ui' as ui;
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:path_provider/path_provider.dart';
import 'package:qr_flutter/qr_flutter.dart';
import 'package:share_plus/share_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
    ),
  );
  runApp(const MyLogoQRApp());
}

class MyLogoQRApp extends StatelessWidget {
  const MyLogoQRApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MyLogoQR',
      debugShowCheckedModeBanner: false,
      themeMode: ThemeMode.dark,
      darkTheme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0F172A),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF6366F1),
          secondary: Color(0xFF10B981),
          surface: Color(0xFF1E293B),
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF0F172A),
          elevation: 0,
          centerTitle: true,
          titleTextStyle: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            letterSpacing: 0.5,
          ),
        ),
        navigationBarTheme: NavigationBarThemeData(
          backgroundColor: const Color(0xFF0B0F19),
          indicatorColor: const Color(0xFF4F46E5).withValues(alpha: 0.4),
          labelTextStyle: WidgetStateProperty.all(
            const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
          ),
        ),
      ),
      home: const MainNavigationScreen(),
    );
  }
}

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  int _currentIndex = 0;

  final List<Widget> _screens = const [
    QRGeneratorScreen(),
    QRScannerScreen(),
    QRHistoryScreen(),
    AboutSettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _currentIndex,
        children: _screens,
      ),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (idx) => setState(() => _currentIndex = idx),
        destinations: const [
          NavigationDestination(
            icon: Icon(Icons.qr_code_2_rounded),
            selectedIcon: Icon(Icons.qr_code_2_rounded, color: Colors.white),
            label: 'Create',
          ),
          NavigationDestination(
            icon: Icon(Icons.qr_code_scanner_rounded),
            selectedIcon: Icon(Icons.qr_code_scanner_rounded, color: Colors.white),
            label: 'Scan',
          ),
          NavigationDestination(
            icon: Icon(Icons.history_rounded),
            selectedIcon: Icon(Icons.history_rounded, color: Colors.white),
            label: 'History',
          ),
          NavigationDestination(
            icon: Icon(Icons.info_outline_rounded),
            selectedIcon: Icon(Icons.info_rounded, color: Colors.white),
            label: 'About',
          ),
        ],
      ),
    );
  }
}

/* =========================================================================
   1. QR GENERATOR SCREEN
   ========================================================================= */
class QRGeneratorScreen extends StatefulWidget {
  const QRGeneratorScreen({super.key});

  @override
  State<QRGeneratorScreen> createState() => _QRGeneratorScreenState();
}

class _QRGeneratorScreenState extends State<QRGeneratorScreen> {
  final GlobalKey _qrRepaintKey = GlobalKey();
  String _selectedType = 'URL';

  // Controllers
  final TextEditingController _urlController = TextEditingController(text: 'https://mylogoqr.com');
  final TextEditingController _textController = TextEditingController();
  final TextEditingController _wifiSsid = TextEditingController();
  final TextEditingController _wifiPass = TextEditingController();
  final TextEditingController _waPhone = TextEditingController();
  final TextEditingController _waMessage = TextEditingController();
  final TextEditingController _vcardName = TextEditingController();
  final TextEditingController _vcardPhone = TextEditingController();
  final TextEditingController _vcardEmail = TextEditingController();

  Color _qrColor = const Color(0xFF0F172A);
  final Color _bgColor = Colors.white;
  File? _customLogoFile;
  bool _useDefaultLogo = true;

  final List<Color> _presetColors = [
    const Color(0xFF0F172A),
    const Color(0xFF4F46E5),
    const Color(0xFF059669),
    const Color(0xFFDC2626),
    const Color(0xFFD97706),
    const Color(0xFF9333EA),
  ];

  String get _currentPayload {
    switch (_selectedType) {
      case 'URL':
        return _urlController.text.trim().isEmpty ? 'https://mylogoqr.com' : _urlController.text.trim();
      case 'WhatsApp':
        final cleanPhone = _waPhone.text.replaceAll(RegExp(r'[^0-9]'), '');
        final msg = Uri.encodeComponent(_waMessage.text.trim());
        return 'https://wa.me/$cleanPhone${msg.isNotEmpty ? "?text=$msg" : ""}';
      case 'Wi-Fi':
        return 'WIFI:T:WPA;S:${_wifiSsid.text.trim()};P:${_wifiPass.text.trim()};;';
      case 'vCard':
        return 'BEGIN:VCARD\nVERSION:3.0\nFN:${_vcardName.text.trim()}\nTEL:${_vcardPhone.text.trim()}\nEMAIL:${_vcardEmail.text.trim()}\nEND:VCARD';
      case 'Text':
      default:
        return _textController.text.trim().isEmpty ? 'MyLogoQR' : _textController.text.trim();
    }
  }

  Future<void> _pickCustomLogo() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.gallery);
    if (picked != null) {
      setState(() {
        _customLogoFile = File(picked.path);
        _useDefaultLogo = false;
      });
    }
  }

  Future<void> _exportAndShare() async {
    try {
      final boundary = _qrRepaintKey.currentContext?.findRenderObject() as RenderRepaintBoundary?;
      if (boundary == null) return;
      final image = await boundary.toImage(pixelRatio: 4.0);
      final byteData = await image.toByteData(format: ui.ImageByteFormat.png);
      if (byteData == null) return;
      final buffer = byteData.buffer.asUint8List();

      final tempDir = await getTemporaryDirectory();
      final file = File('${tempDir.path}/mylogoqr_${DateTime.now().millisecondsSinceEpoch}.png');
      await file.writeAsBytes(buffer);

      await SharePlus.instance.share(ShareParams(files: [XFile(file.path)], text: 'Generated with MyLogoQR (100% Free & Private)'));
      _saveToHistory(_currentPayload, 'Created');
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Share failed: $e')));
      }
    }
  }

  Future<void> _saveToHistory(String payload, String type) async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList('qr_history') ?? [];
    final item = jsonEncode({
      'payload': payload,
      'type': type,
      'category': _selectedType,
      'time': DateTime.now().toIso8601String(),
    });
    list.insert(0, item);
    await prefs.setStringList('qr_history', list);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.all(4),
              decoration: BoxDecoration(
                color: const Color(0xFF6366F1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: const Icon(Icons.qr_code_2_rounded, size: 20, color: Colors.white),
            ),
            const SizedBox(width: 8),
            const Text('MyLogoQR', style: TextStyle(fontWeight: FontWeight.bold)),
          ],
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // QR Type Chips
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: ['URL', 'WhatsApp', 'Wi-Fi', 'vCard', 'Text'].map((type) {
                  final isSelected = _selectedType == type;
                  return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ChoiceChip(
                      label: Text(type),
                      selected: isSelected,
                      selectedColor: const Color(0xFF4F46E5),
                      labelStyle: TextStyle(
                        color: isSelected ? Colors.white : Colors.grey[300],
                        fontWeight: FontWeight.w600,
                      ),
                      onSelected: (val) {
                        if (val) setState(() => _selectedType = type);
                      },
                    ),
                  );
                }).toList(),
              ),
            ),
            const SizedBox(height: 16),

            // Dynamic Inputs Card
            Card(
              color: const Color(0xFF1E293B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: _buildInputs(),
              ),
            ),
            const SizedBox(height: 16),

            // Customization: Logo & Color
            Card(
              color: const Color(0xFF1E293B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Custom Logo & Colors', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        OutlinedButton.icon(
                          onPressed: _pickCustomLogo,
                          icon: const Icon(Icons.add_photo_alternate_rounded, size: 18),
                          label: Text(_customLogoFile != null ? 'Change Logo' : 'Custom Logo'),
                          style: OutlinedButton.styleFrom(
                            foregroundColor: Colors.white,
                            side: const BorderSide(color: Color(0xFF6366F1)),
                          ),
                        ),
                        const SizedBox(width: 10),
                        if (_customLogoFile != null)
                          TextButton(
                            onPressed: () => setState(() => _customLogoFile = null),
                            child: const Text('Remove', style: TextStyle(color: Colors.redAccent)),
                          ),
                      ],
                    ),
                    const SizedBox(height: 14),
                    const Text('QR Code Color', style: TextStyle(fontSize: 13, color: Colors.grey)),
                    const SizedBox(height: 8),
                    Row(
                      children: _presetColors.map((color) {
                        final isSelected = _qrColor == color;
                        return GestureDetector(
                          onTap: () => setState(() => _qrColor = color),
                          child: Container(
                            margin: const EdgeInsets.only(right: 10),
                            width: 32,
                            height: 32,
                            decoration: BoxDecoration(
                              color: color,
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: isSelected ? Colors.white : Colors.transparent,
                                width: 2.5,
                              ),
                            ),
                            child: isSelected ? const Icon(Icons.check, size: 16, color: Colors.white) : null,
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Live QR Preview Container
            Center(
              child: RepaintBoundary(
                key: _qrRepaintKey,
                child: Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: _bgColor,
                    borderRadius: BorderRadius.circular(24),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.3),
                        blurRadius: 20,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      QrImageView(
                        data: _currentPayload,
                        version: QrVersions.auto,
                        size: 220,
                        backgroundColor: Colors.transparent,
                        eyeStyle: QrEyeStyle(
                          eyeShape: QrEyeShape.square,
                          color: _qrColor,
                        ),
                        dataModuleStyle: QrDataModuleStyle(
                          dataModuleShape: QrDataModuleShape.square,
                          color: _qrColor,
                        ),
                        errorCorrectionLevel: QrErrorCorrectLevel.Q,
                      ),
                      if (_customLogoFile != null)
                        Container(
                          width: 48,
                          height: 48,
                          padding: const EdgeInsets.all(4),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(10),
                            boxShadow: [
                              BoxShadow(color: Colors.black.withValues(alpha: 0.2), blurRadius: 4),
                            ],
                          ),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: Image.file(_customLogoFile!, fit: BoxFit.cover),
                          ),
                        )
                      else if (_useDefaultLogo)
                        Container(
                          width: 46,
                          height: 46,
                          padding: const EdgeInsets.all(3),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            borderRadius: BorderRadius.circular(10),
                            boxShadow: [
                              BoxShadow(color: Colors.black.withValues(alpha: 0.2), blurRadius: 4),
                            ],
                          ),
                          child: ClipRRect(
                            borderRadius: BorderRadius.circular(8),
                            child: Image.asset('assets/logo.png', fit: BoxFit.cover),
                          ),
                        ),
                    ],
                  ),
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Export Actions
            ElevatedButton.icon(
              onPressed: _exportAndShare,
              icon: const Icon(Icons.share_rounded),
              label: const Text('Export & Share High-Res QR', style: TextStyle(fontWeight: FontWeight.bold)),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF4F46E5),
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildInputs() {
    switch (_selectedType) {
      case 'URL':
        return TextField(
          controller: _urlController,
          decoration: const InputDecoration(
            labelText: 'Website URL',
            hintText: 'https://example.com',
            prefixIcon: Icon(Icons.link_rounded),
          ),
          onChanged: (_) => setState(() {}),
        );
      case 'WhatsApp':
        return Column(
          children: [
            TextField(
              controller: _waPhone,
              keyboardType: TextInputType.phone,
              decoration: const InputDecoration(
                labelText: 'Phone with Country Code',
                hintText: '923001234567',
                prefixIcon: Icon(Icons.phone_rounded),
              ),
              onChanged: (_) => setState(() {}),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _waMessage,
              decoration: const InputDecoration(
                labelText: 'Pre-filled Message (Optional)',
                hintText: 'Hello, I scanned your QR code!',
                prefixIcon: Icon(Icons.message_rounded),
              ),
              onChanged: (_) => setState(() {}),
            ),
          ],
        );
      case 'Wi-Fi':
        return Column(
          children: [
            TextField(
              controller: _wifiSsid,
              decoration: const InputDecoration(
                labelText: 'Network Name (SSID)',
                prefixIcon: Icon(Icons.wifi_rounded),
              ),
              onChanged: (_) => setState(() {}),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _wifiPass,
              obscureText: true,
              decoration: const InputDecoration(
                labelText: 'Wi-Fi Password',
                prefixIcon: Icon(Icons.lock_outline_rounded),
              ),
              onChanged: (_) => setState(() {}),
            ),
          ],
        );
      case 'vCard':
        return Column(
          children: [
            TextField(
              controller: _vcardName,
              decoration: const InputDecoration(
                labelText: 'Full Name',
                prefixIcon: Icon(Icons.person_rounded),
              ),
              onChanged: (_) => setState(() {}),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _vcardPhone,
              keyboardType: TextInputType.phone,
              decoration: const InputDecoration(
                labelText: 'Phone Number',
                prefixIcon: Icon(Icons.phone_rounded),
              ),
              onChanged: (_) => setState(() {}),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _vcardEmail,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(
                labelText: 'Email Address',
                prefixIcon: Icon(Icons.email_rounded),
              ),
              onChanged: (_) => setState(() {}),
            ),
          ],
        );
      case 'Text':
      default:
        return TextField(
          controller: _textController,
          maxLines: 3,
          decoration: const InputDecoration(
            labelText: 'Text Content',
            hintText: 'Enter any text, notes, or instructions...',
            prefixIcon: Icon(Icons.notes_rounded),
          ),
          onChanged: (_) => setState(() {}),
        );
    }
  }
}

/* =========================================================================
   2. QR CAMERA SCANNER SCREEN
   ========================================================================= */
class QRScannerScreen extends StatefulWidget {
  const QRScannerScreen({super.key});

  @override
  State<QRScannerScreen> createState() => _QRScannerScreenState();
}

class _QRScannerScreenState extends State<QRScannerScreen> {
  final MobileScannerController _cameraController = MobileScannerController();
  bool _isTorchOn = false;
  bool _isProcessing = false;

  void _onDetect(BarcodeCapture capture) {
    if (_isProcessing) return;
    final barcodes = capture.barcodes;
    if (barcodes.isEmpty) return;

    final rawValue = barcodes.first.rawValue;
    if (rawValue == null || rawValue.isEmpty) return;

    _isProcessing = true;
    HapticFeedback.mediumImpact();
    _saveScanHistory(rawValue);

    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E293B),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      builder: (ctx) {
        final isUrl = rawValue.startsWith('http://') || rawValue.startsWith('https://');
        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: const Color(0xFF10B981).withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.check_circle_rounded, color: Color(0xFF10B981)),
                  ),
                  const SizedBox(width: 12),
                  const Text('QR Code Scanned', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                ],
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: const Color(0xFF0F172A),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: SelectableText(
                  rawValue,
                  style: const TextStyle(fontSize: 14, color: Colors.white70),
                ),
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  if (isUrl) ...[
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () async {
                          final uri = Uri.parse(rawValue);
                          if (await canLaunchUrl(uri)) {
                            await launchUrl(uri, mode: LaunchMode.externalApplication);
                          }
                        },
                        icon: const Icon(Icons.open_in_browser_rounded),
                        label: const Text('Open URL'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF4F46E5),
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                  ],
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: () {
                        Clipboard.setData(ClipboardData(text: rawValue));
                        Navigator.pop(ctx);
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Copied to clipboard!')),
                        );
                      },
                      icon: const Icon(Icons.copy_rounded),
                      label: const Text('Copy'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
            ],
          ),
        );
      },
    ).whenComplete(() {
      Future.delayed(const Duration(seconds: 1), () {
        if (mounted) setState(() => _isProcessing = false);
      });
    });
  }

  Future<void> _saveScanHistory(String payload) async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList('qr_history') ?? [];
    final item = jsonEncode({
      'payload': payload,
      'type': 'Scanned',
      'category': payload.startsWith('http') ? 'URL' : 'Text',
      'time': DateTime.now().toIso8601String(),
    });
    list.insert(0, item);
    await prefs.setStringList('qr_history', list);
  }

  @override
  void dispose() {
    _cameraController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Live QR Scanner'),
        actions: [
          IconButton(
            icon: Icon(_isTorchOn ? Icons.flash_on_rounded : Icons.flash_off_rounded),
            onPressed: () {
              _cameraController.toggleTorch();
              setState(() => _isTorchOn = !_isTorchOn);
            },
          ),
          IconButton(
            icon: const Icon(Icons.flip_camera_ios_rounded),
            onPressed: () => _cameraController.switchCamera(),
          ),
        ],
      ),
      body: Stack(
        children: [
          MobileScanner(
            controller: _cameraController,
            onDetect: _onDetect,
          ),
          // Scanner Overlay Frame
          Center(
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                border: Border.all(color: const Color(0xFF6366F1), width: 3),
                borderRadius: BorderRadius.circular(20),
              ),
            ),
          ),
          Positioned(
            bottom: 40,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 20),
              decoration: BoxDecoration(
                color: Colors.black.withValues(alpha: 0.7),
                borderRadius: BorderRadius.circular(30),
              ),
              child: const Text(
                'Point camera at any QR code to scan',
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.w500),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/* =========================================================================
   3. QR HISTORY SCREEN
   ========================================================================= */
class QRHistoryScreen extends StatefulWidget {
  const QRHistoryScreen({super.key});

  @override
  State<QRHistoryScreen> createState() => _QRHistoryScreenState();
}

class _QRHistoryScreenState extends State<QRHistoryScreen> {
  List<Map<String, dynamic>> _history = [];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final list = prefs.getStringList('qr_history') ?? [];
    setState(() {
      _history = list.map((e) => jsonDecode(e) as Map<String, dynamic>).toList();
    });
  }

  Future<void> _clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('qr_history');
    setState(() => _history.clear());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('History & Saved'),
        actions: [
          if (_history.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.delete_sweep_rounded),
              onPressed: _clearHistory,
            ),
        ],
      ),
      body: _history.isEmpty
          ? Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(Icons.history_rounded, size: 64, color: Colors.grey[600]),
                  const SizedBox(height: 12),
                  const Text('No QR history yet', style: TextStyle(color: Colors.grey, fontSize: 16)),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              itemCount: _history.length,
              itemBuilder: (ctx, idx) {
                final item = _history[idx];
                final isCreated = item['type'] == 'Created';
                return Card(
                  color: const Color(0xFF1E293B),
                  margin: const EdgeInsets.only(bottom: 10),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: isCreated
                          ? const Color(0xFF4F46E5).withValues(alpha: 0.2)
                          : const Color(0xFF10B981).withValues(alpha: 0.2),
                      child: Icon(
                        isCreated ? Icons.qr_code_2_rounded : Icons.qr_code_scanner_rounded,
                        color: isCreated ? const Color(0xFF818CF8) : const Color(0xFF34D399),
                        size: 20,
                      ),
                    ),
                    title: Text(
                      item['payload'] ?? '',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
                    ),
                    subtitle: Text(
                      '${item['type']} • ${item['category'] ?? 'QR'}',
                      style: const TextStyle(fontSize: 12, color: Colors.grey),
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.copy_rounded, size: 18),
                      onPressed: () {
                        Clipboard.setData(ClipboardData(text: item['payload'] ?? ''));
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Copied payload to clipboard')),
                        );
                      },
                    ),
                  ),
                );
              },
            ),
    );
  }
}

/* =========================================================================
   4. ABOUT & PRIVACY SCREEN
   ========================================================================= */
class AboutSettingsScreen extends StatelessWidget {
  const AboutSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('About MyLogoQR')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(color: Colors.black.withValues(alpha: 0.3), blurRadius: 10),
                ],
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(16),
                child: Image.asset('assets/logo.png', width: 90, height: 90, fit: BoxFit.cover),
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'MyLogoQR',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const Text(
              'Version 1.1.0 • Native Android Edition',
              style: TextStyle(color: Color(0xFF94A3B8), fontSize: 13),
            ),
            const SizedBox(height: 24),

            // Privacy Card
            Card(
              color: const Color(0xFF1E293B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: const Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.security_rounded, color: Color(0xFF10B981)),
                        SizedBox(width: 8),
                        Text('100% Privacy-First Architecture', style: TextStyle(fontWeight: FontWeight.bold)),
                      ],
                    ),
                    SizedBox(height: 10),
                    Text(
                      'All QR codes, custom logos, and camera scanning happen strictly inside your phone memory. Zero telemetry, zero analytics tracking, and no cloud servers.',
                      style: TextStyle(color: Colors.white70, fontSize: 13, height: 1.5),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),

            // Links Card
            Card(
              color: const Color(0xFF1E293B),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Column(
                children: [
                  ListTile(
                    leading: const Icon(Icons.language_rounded, color: Color(0xFF6366F1)),
                    title: const Text('Visit Official Website'),
                    subtitle: const Text('https://mylogoqr.com'),
                    trailing: const Icon(Icons.chevron_right_rounded),
                    onTap: () => launchUrl(Uri.parse('https://mylogoqr.com'), mode: LaunchMode.externalApplication),
                  ),
                  const Divider(color: Colors.white10, height: 1),
                  ListTile(
                    leading: const Icon(Icons.star_rate_rounded, color: Colors.amber),
                    title: const Text('Rate on Google Play'),
                    subtitle: const Text('com.mylogoqr.app'),
                    trailing: const Icon(Icons.chevron_right_rounded),
                    onTap: () => launchUrl(
                      Uri.parse('https://play.google.com/store/apps/details?id=com.mylogoqr.app'),
                      mode: LaunchMode.externalApplication,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),
            const Text(
              'Engineered by SRK AMD • 100% Free Forever',
              style: TextStyle(color: Colors.grey, fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }
}
