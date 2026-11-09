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
      systemNavigationBarColor: Color(0xFF090D16),
      systemNavigationBarIconBrightness: Brightness.light,
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
        scaffoldBackgroundColor: const Color(0xFF090D16),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF6366F1),
          secondary: Color(0xFF10B981),
          surface: Color(0xFF131B2E),
        ),
        fontFamily: 'Roboto',
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xFF090D16),
          elevation: 0,
          centerTitle: true,
          titleTextStyle: TextStyle(
            fontSize: 19,
            fontWeight: FontWeight.w700,
            letterSpacing: 0.3,
            color: Colors.white,
          ),
        ),
        navigationBarTheme: NavigationBarThemeData(
          backgroundColor: const Color(0xFF060910),
          indicatorColor: const Color(0xFF4F46E5).withValues(alpha: 0.35),
          labelTextStyle: WidgetStateProperty.all(
            const TextStyle(fontSize: 11, fontWeight: FontWeight.w600, color: Color(0xFF94A3B8)),
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
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          border: Border(top: BorderSide(color: Color(0xFF1E293B), width: 1)),
        ),
        child: NavigationBar(
          selectedIndex: _currentIndex,
          height: 68,
          onDestinationSelected: (idx) => setState(() => _currentIndex = idx),
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.qr_code_2_rounded),
              selectedIcon: Icon(Icons.qr_code_2_rounded, color: Color(0xFF818CF8)),
              label: 'Create',
            ),
            NavigationDestination(
              icon: Icon(Icons.qr_code_scanner_rounded),
              selectedIcon: Icon(Icons.qr_code_scanner_rounded, color: Color(0xFF818CF8)),
              label: 'Scan',
            ),
            NavigationDestination(
              icon: Icon(Icons.history_rounded),
              selectedIcon: Icon(Icons.history_rounded, color: Color(0xFF818CF8)),
              label: 'History',
            ),
            NavigationDestination(
              icon: Icon(Icons.tune_rounded),
              selectedIcon: Icon(Icons.tune_rounded, color: Color(0xFF818CF8)),
              label: 'About',
            ),
          ],
        ),
      ),
    );
  }
}

/* =========================================================================
   1. QR GENERATOR SCREEN - Sleek Modern SaaS Design
   ========================================================================= */
class QRGeneratorScreen extends StatefulWidget {
  const QRGeneratorScreen({super.key});

  @override
  State<QRGeneratorScreen> createState() => _QRGeneratorScreenState();
}

class _QRGeneratorScreenState extends State<QRGeneratorScreen> {
  final GlobalKey _qrRepaintKey = GlobalKey();
  String _selectedType = 'URL';

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

  final TextEditingController _badgeController = TextEditingController(text: 'SCAN ME');
  bool _showBadge = true;
  String _badgeStyle = 'pill'; // 'pill', 'outline', 'clean' 

  final List<Color> _presetColors = [
    const Color(0xFF0F172A),
    const Color(0xFF4F46E5),
    const Color(0xFF059669),
    const Color(0xFFDC2626),
    const Color(0xFFD97706),
    const Color(0xFF7C3AED),
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
      setState(() => _customLogoFile = File(picked.path));
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

      await Share.shareXFiles([XFile(file.path)], text: 'Created with MyLogoQR (100% Free & Private)');
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
              padding: const EdgeInsets.all(6),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [Color(0xFF6366F1), Color(0xFF4F46E5)]),
                borderRadius: BorderRadius.circular(10),
              ),
              child: const Icon(Icons.qr_code_2_rounded, size: 20, color: Colors.white),
            ),
            const SizedBox(width: 10),
            const Text('MyLogoQR Studio', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 18)),
          ],
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Category Selector Chips
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildTypeChip('URL', Icons.language_rounded),
                  _buildTypeChip('WhatsApp', Icons.chat_rounded),
                  _buildTypeChip('Wi-Fi', Icons.wifi_rounded),
                  _buildTypeChip('vCard', Icons.badge_rounded),
                  _buildTypeChip('Text', Icons.short_text_rounded),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Inputs Glass Card
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFF131B2E),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFF1E293B), width: 1.2),
              ),
              child: _buildInputs(),
            ),
            const SizedBox(height: 16),

            // Customization Card
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFF131B2E),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFF1E293B), width: 1.2),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Brand Logo & Colors', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15, color: Colors.white)),
                  const SizedBox(height: 14),
                  Row(
                    children: [
                      ElevatedButton.icon(
                        onPressed: _pickCustomLogo,
                        icon: const Icon(Icons.add_photo_alternate_rounded, size: 18),
                        label: Text(_customLogoFile != null ? 'Change Logo' : 'Upload Logo'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: const Color(0xFF1E293B),
                          foregroundColor: Colors.white,
                          side: const BorderSide(color: Color(0xFF4F46E5), width: 1.2),
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                        ),
                      ),
                      const SizedBox(width: 12),
                      if (_customLogoFile != null)
                        TextButton.icon(
                          onPressed: () => setState(() => _customLogoFile = null),
                          icon: const Icon(Icons.close_rounded, size: 16, color: Colors.redAccent),
                          label: const Text('Remove', style: TextStyle(color: Colors.redAccent)),
                        ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  const Text('QR Matrix Color', style: TextStyle(fontSize: 12, color: Color(0xFF94A3B8), fontWeight: FontWeight.w600)),
                  const SizedBox(height: 10),
                  Row(
                    children: _presetColors.map((color) {
                      final isSelected = _qrColor == color;
                      return GestureDetector(
                        onTap: () => setState(() => _qrColor = color),
                        child: Container(
                          margin: const EdgeInsets.only(right: 12),
                          width: 34,
                          height: 34,
                          decoration: BoxDecoration(
                            color: color,
                            shape: BoxShape.circle,
                            border: Border.all(
                              color: isSelected ? Colors.white : Colors.transparent,
                              width: 2.5,
                            ),
                            boxShadow: isSelected
                                ? [BoxShadow(color: color.withValues(alpha: 0.6), blurRadius: 10, spreadRadius: 1)]
                                : null,
                          ),
                          child: isSelected ? const Icon(Icons.check, size: 16, color: Colors.white) : null,
                        ),
                      );
                    }).toList(),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // 6. Label Under QR (Scan Me Brand Badge)
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFF131B2E),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFF1E293B), width: 1.2),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.label_important_rounded, size: 20, color: Color(0xFF818CF8)),
                          SizedBox(width: 8),
                          Text('Label under QR (Brand Badge)', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15, color: Colors.white)),
                        ],
                      ),
                      Switch(
                        value: _showBadge,
                        activeColor: const Color(0xFF6366F1),
                        onChanged: (val) => setState(() => _showBadge = val),
                      ),
                    ],
                  ),
                  if (_showBadge) ...[
                    const SizedBox(height: 12),
                    TextField(
                      controller: _badgeController,
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                      decoration: InputDecoration(
                        hintText: 'SCAN ME, FOR MENU, WI-FI',
                        hintStyle: const TextStyle(color: Color(0xFF64748B)),
                        prefixIcon: const Icon(Icons.edit_rounded, color: Color(0xFF6366F1), size: 18),
                        filled: true,
                        fillColor: const Color(0xFF090D16),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                          borderSide: const BorderSide(color: Color(0xFF1E293B)),
                        ),
                        contentPadding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                      ),
                      onChanged: (_) => setState(() {}),
                    ),
                    const SizedBox(height: 10),
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      child: Row(
                        children: ['SCAN ME', 'SCAN FOR MENU', 'CONNECT WI-FI', 'ORDER HERE', 'PAY HERE'].map((text) {
                          return Padding(
                            padding: const EdgeInsets.only(right: 8),
                            child: ActionChip(
                              label: Text(text),
                              backgroundColor: const Color(0xFF090D16),
                              side: const BorderSide(color: Color(0xFF1E293B)),
                              labelStyle: const TextStyle(color: Color(0xFFCBD5E1), fontSize: 11, fontWeight: FontWeight.w600),
                              onPressed: () {
                                setState(() => _badgeController.text = text);
                              },
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                    const SizedBox(height: 14),
                    Row(
                      children: [
                        _buildBadgeStyleOption('pill', 'Pill Badge'),
                        const SizedBox(width: 8),
                        _buildBadgeStyleOption('outline', 'Outline'),
                        const SizedBox(width: 8),
                        _buildBadgeStyleOption('clean', 'Clean Text'),
                      ],
                    ),
                  ],
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Live QR Preview
            Center(
              child: Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(30),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF6366F1).withValues(alpha: 0.15),
                      blurRadius: 30,
                      spreadRadius: 2,
                    ),
                  ],
                ),
                child: RepaintBoundary(
                  key: _qrRepaintKey,
                  child: Container(
                    padding: const EdgeInsets.fromLTRB(20, 20, 20, 18),
                    decoration: BoxDecoration(
                      color: _bgColor,
                      borderRadius: BorderRadius.circular(24),
                    ),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Stack(
                          alignment: Alignment.center,
                          children: [
                            QrImageView(
                              data: _currentPayload,
                              version: QrVersions.auto,
                              size: 210,
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
                                    BoxShadow(color: Colors.black.withValues(alpha: 0.25), blurRadius: 6),
                                  ],
                                ),
                                child: ClipRRect(
                                  borderRadius: BorderRadius.circular(8),
                                  child: Image.file(_customLogoFile!, fit: BoxFit.cover),
                                ),
                              )
                            else
                              Container(
                                width: 44,
                                height: 44,
                                padding: const EdgeInsets.all(4),
                                decoration: BoxDecoration(
                                  color: Colors.white,
                                  borderRadius: BorderRadius.circular(10),
                                  boxShadow: [
                                    BoxShadow(color: Colors.black.withValues(alpha: 0.2), blurRadius: 5),
                                  ],
                                ),
                                child: ClipRRect(
                                  borderRadius: BorderRadius.circular(7),
                                  child: Image.asset('assets/logo.png', fit: BoxFit.cover),
                                ),
                              ),
                          ],
                        ),
                        if (_showBadge && _badgeController.text.trim().isNotEmpty)
                          _buildScanMeBadge(),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Share Action Button
            Container(
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF4F46E5), Color(0xFF7C3AED)],
                  begin: Alignment.centerLeft,
                  end: Alignment.centerRight,
                ),
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(color: const Color(0xFF4F46E5).withValues(alpha: 0.35), blurRadius: 16, offset: const Offset(0, 6)),
                ],
              ),
              child: ElevatedButton.icon(
                onPressed: _exportAndShare,
                icon: const Icon(Icons.share_rounded, size: 20),
                label: const Text('Export & Share High-Res QR', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.transparent,
                  shadowColor: Colors.transparent,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                ),
              ),
            ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }

  Widget _buildBadgeStyleOption(String style, String label) {
    final isSelected = _badgeStyle == style;
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => _badgeStyle = style),
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 9),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFF4F46E5).withValues(alpha: 0.35) : const Color(0xFF090D16),
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
              color: isSelected ? const Color(0xFF6366F1) : const Color(0xFF1E293B),
              width: 1.2,
            ),
          ),
          alignment: Alignment.center,
          child: Text(
            label,
            style: TextStyle(
              fontSize: 11,
              fontWeight: FontWeight.w700,
              color: isSelected ? Colors.white : const Color(0xFF94A3B8),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildScanMeBadge() {
    final text = _badgeController.text.trim().toUpperCase();
    if (text.isEmpty) return const SizedBox.shrink();

    if (_badgeStyle == 'pill') {
      return Container(
        margin: const EdgeInsets.only(top: 14),
        padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 8),
        decoration: BoxDecoration(
          color: _qrColor,
          borderRadius: BorderRadius.circular(99),
          boxShadow: [
            BoxShadow(
              color: _qrColor.withValues(alpha: 0.25),
              blurRadius: 8,
              offset: const Offset(0, 3),
            ),
          ],
        ),
        child: Text(
          text,
          style: const TextStyle(
            color: Colors.white,
            fontWeight: FontWeight.w800,
            fontSize: 13,
            letterSpacing: 2.0,
          ),
        ),
      );
    } else if (_badgeStyle == 'outline') {
      return Container(
        margin: const EdgeInsets.only(top: 14),
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 6),
        decoration: BoxDecoration(
          border: Border.all(color: _qrColor, width: 2),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Text(
          text,
          style: TextStyle(
            color: _qrColor,
            fontWeight: FontWeight.w800,
            fontSize: 13,
            letterSpacing: 2.0,
          ),
        ),
      );
    } else {
      return Padding(
        padding: const EdgeInsets.only(top: 12),
        child: Text(
          text,
          style: TextStyle(
            color: _qrColor,
            fontWeight: FontWeight.w800,
            fontSize: 14,
            letterSpacing: 2.5,
          ),
        ),
      );
    }
  }

  Widget _buildTypeChip(String type, IconData icon) {
    final isSelected = _selectedType == type;
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: GestureDetector(
        onTap: () => setState(() => _selectedType = type),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 9),
          decoration: BoxDecoration(
            color: isSelected ? const Color(0xFF4F46E5) : const Color(0xFF131B2E),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(
              color: isSelected ? const Color(0xFF6366F1) : const Color(0xFF1E293B),
            ),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 16, color: isSelected ? Colors.white : const Color(0xFF94A3B8)),
              const SizedBox(width: 6),
              Text(
                type,
                style: TextStyle(
                  color: isSelected ? Colors.white : const Color(0xFF94A3B8),
                  fontWeight: FontWeight.w600,
                  fontSize: 13,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInputs() {
    switch (_selectedType) {
      case 'URL':
        return TextField(
          controller: _urlController,
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            labelText: 'Website URL',
            labelStyle: TextStyle(color: Color(0xFF94A3B8)),
            hintText: 'https://example.com',
            prefixIcon: Icon(Icons.link_rounded, color: Color(0xFF6366F1)),
            border: InputBorder.none,
          ),
          onChanged: (_) => setState(() {}),
        );
      case 'WhatsApp':
        return Column(
          children: [
            TextField(
              controller: _waPhone,
              keyboardType: TextInputType.phone,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Phone with Country Code',
                labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                hintText: '923001234567',
                prefixIcon: Icon(Icons.phone_rounded, color: Color(0xFF10B981)),
                border: InputBorder.none,
              ),
              onChanged: (_) => setState(() {}),
            ),
            const Divider(color: Color(0xFF1E293B)),
            TextField(
              controller: _waMessage,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Pre-filled Message (Optional)',
                labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                hintText: 'Hello, I scanned your QR code!',
                prefixIcon: Icon(Icons.message_rounded, color: Color(0xFF10B981)),
                border: InputBorder.none,
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
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Wi-Fi Network Name (SSID)',
                labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                prefixIcon: Icon(Icons.wifi_rounded, color: Color(0xFF6366F1)),
                border: InputBorder.none,
              ),
              onChanged: (_) => setState(() {}),
            ),
            const Divider(color: Color(0xFF1E293B)),
            TextField(
              controller: _wifiPass,
              obscureText: true,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Wi-Fi Password',
                labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                prefixIcon: Icon(Icons.lock_outline_rounded, color: Color(0xFF6366F1)),
                border: InputBorder.none,
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
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Full Name',
                labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                prefixIcon: Icon(Icons.person_rounded, color: Color(0xFF6366F1)),
                border: InputBorder.none,
              ),
              onChanged: (_) => setState(() {}),
            ),
            const Divider(color: Color(0xFF1E293B)),
            TextField(
              controller: _vcardPhone,
              keyboardType: TextInputType.phone,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Phone Number',
                labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                prefixIcon: Icon(Icons.phone_rounded, color: Color(0xFF6366F1)),
                border: InputBorder.none,
              ),
              onChanged: (_) => setState(() {}),
            ),
            const Divider(color: Color(0xFF1E293B)),
            TextField(
              controller: _vcardEmail,
              keyboardType: TextInputType.emailAddress,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: 'Email Address',
                labelStyle: TextStyle(color: Color(0xFF94A3B8)),
                prefixIcon: Icon(Icons.email_rounded, color: Color(0xFF6366F1)),
                border: InputBorder.none,
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
          style: const TextStyle(color: Colors.white),
          decoration: const InputDecoration(
            labelText: 'Text Content',
            labelStyle: TextStyle(color: Color(0xFF94A3B8)),
            hintText: 'Enter text, notes, instructions...',
            prefixIcon: Icon(Icons.notes_rounded, color: Color(0xFF6366F1)),
            border: InputBorder.none,
          ),
          onChanged: (_) => setState(() {}),
        );
    }
  }
}

/* =========================================================================
   2. QR CAMERA SCANNER SCREEN - Immersive Pro Viewfinder & High Bottom Sheet
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

  void _onDetect(BarcodeCapture capture) async {
    if (_isProcessing) return;
    final barcodes = capture.barcodes;
    if (barcodes.isEmpty) return;

    final rawValue = barcodes.first.rawValue;
    if (rawValue == null || rawValue.trim().isEmpty) return;

    _isProcessing = true;
    HapticFeedback.mediumImpact();
    _saveScanHistory(rawValue.trim());

    // Stop camera so it does not freeze phone GPU/CPU
    try {
      await _cameraController.stop();
    } catch (_) {}

    if (!mounted) return;

    final cleanRaw = rawValue.trim();
    final isUrl = cleanRaw.startsWith('http://') || cleanRaw.startsWith('https://') || cleanRaw.contains('.');

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF131B2E),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(28)),
      ),
      builder: (ctx) {
        return SafeArea(
          bottom: true,
          top: false,
          child: Padding(
            padding: const EdgeInsets.fromLTRB(22, 20, 22, 36), // High bottom padding for system bar
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Center(
                  child: Container(
                    width: 44,
                    height: 4,
                    margin: const EdgeInsets.only(bottom: 18),
                    decoration: BoxDecoration(
                      color: Colors.white24,
                      borderRadius: BorderRadius.circular(99),
                    ),
                  ),
                ),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: const Color(0xFF10B981).withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(Icons.check_circle_rounded, color: Color(0xFF10B981), size: 24),
                    ),
                    const SizedBox(width: 12),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('QR Code Detected', style: TextStyle(fontSize: 17, fontWeight: FontWeight.w700, color: Colors.white)),
                        Text(
                          isUrl ? 'Website Link' : 'Plain Content',
                          style: const TextStyle(fontSize: 12, color: Color(0xFF94A3B8)),
                        ),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 18),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: const Color(0xFF090D16),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: const Color(0xFF1E293B)),
                  ),
                  child: SelectableText(
                    cleanRaw,
                    style: const TextStyle(fontSize: 14, color: Colors.white, height: 1.45, fontWeight: FontWeight.w500),
                  ),
                ),
                const SizedBox(height: 24),
                Row(
                  children: [
                    if (isUrl) ...[
                      Expanded(
                        child: Container(
                          decoration: BoxDecoration(
                            gradient: const LinearGradient(colors: [Color(0xFF4F46E5), Color(0xFF7C3AED)]),
                            borderRadius: BorderRadius.circular(14),
                            boxShadow: [
                              BoxShadow(color: const Color(0xFF4F46E5).withValues(alpha: 0.35), blurRadius: 12, offset: const Offset(0, 4)),
                            ],
                          ),
                          child: ElevatedButton.icon(
                            onPressed: () async {
                              Navigator.pop(ctx);
                              try {
                                final target = cleanRaw.startsWith('http') ? cleanRaw : 'https://$cleanRaw';
                                await launchUrl(Uri.parse(target), mode: LaunchMode.externalApplication);
                              } catch (e) {
                                if (mounted) {
                                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Cannot open: $e')));
                                }
                              }
                            },
                            icon: const Icon(Icons.open_in_browser_rounded, size: 20),
                            label: const Text('Open URL', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.transparent,
                              shadowColor: Colors.transparent,
                              foregroundColor: Colors.white,
                              padding: const EdgeInsets.symmetric(vertical: 16),
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                            ),
                          ),
                        ),
                      ),
                      const SizedBox(width: 12),
                    ],
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: () async {
                          final messenger = ScaffoldMessenger.of(context);
                          await Clipboard.setData(ClipboardData(text: cleanRaw));
                          HapticFeedback.lightImpact();
                          if (ctx.mounted) Navigator.pop(ctx);
                          messenger.showSnackBar(
                            const SnackBar(
                              content: Row(
                                children: [
                                  Icon(Icons.check_circle_rounded, color: Color(0xFF10B981), size: 18),
                                  SizedBox(width: 8),
                                  Text('Copied to clipboard!'),
                                ],
                              ),
                              backgroundColor: Color(0xFF1E293B),
                              behavior: SnackBarBehavior.floating,
                              duration: Duration(seconds: 2),
                            ),
                          );
                        },
                        icon: const Icon(Icons.copy_rounded, size: 20),
                        label: const Text('Copy', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15)),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: Colors.white,
                          side: const BorderSide(color: Color(0xFF334155), width: 1.5),
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    ).whenComplete(() async {
      try {
        await _cameraController.start();
      } catch (_) {}
      if (mounted) setState(() => _isProcessing = false);
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
          Container(
            margin: const EdgeInsets.only(right: 8),
            decoration: BoxDecoration(
              color: const Color(0xFF131B2E),
              shape: BoxShape.circle,
              border: Border.all(color: const Color(0xFF1E293B)),
            ),
            child: IconButton(
              icon: Icon(_isTorchOn ? Icons.flash_on_rounded : Icons.flash_off_rounded, size: 20),
              color: _isTorchOn ? Colors.amber : Colors.white,
              onPressed: () {
                _cameraController.toggleTorch();
                setState(() => _isTorchOn = !_isTorchOn);
              },
            ),
          ),
          Container(
            margin: const EdgeInsets.only(right: 12),
            decoration: BoxDecoration(
              color: const Color(0xFF131B2E),
              shape: BoxShape.circle,
              border: Border.all(color: const Color(0xFF1E293B)),
            ),
            child: IconButton(
              icon: const Icon(Icons.flip_camera_ios_rounded, size: 20, color: Colors.white),
              onPressed: () => _cameraController.switchCamera(),
            ),
          ),
        ],
      ),
      body: Stack(
        children: [
          MobileScanner(
            controller: _cameraController,
            onDetect: _onDetect,
          ),
          // Viewfinder Glow Target Frame
          Center(
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                border: Border.all(color: const Color(0xFF6366F1), width: 2.5),
                borderRadius: BorderRadius.circular(24),
                boxShadow: [
                  BoxShadow(
                    color: const Color(0xFF6366F1).withValues(alpha: 0.3),
                    blurRadius: 20,
                    spreadRadius: 2,
                  ),
                ],
              ),
            ),
          ),
          // Bottom Helper Pill
          Positioned(
            bottom: 36,
            left: 28,
            right: 28,
            child: Container(
              padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
              decoration: BoxDecoration(
                color: const Color(0xFF090D16).withValues(alpha: 0.85),
                borderRadius: BorderRadius.circular(99),
                border: Border.all(color: Colors.white12),
              ),
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.center_focus_strong_rounded, size: 18, color: Color(0xFF818CF8)),
                  SizedBox(width: 8),
                  Text(
                    'Align QR code inside the frame to scan',
                    style: TextStyle(color: Colors.white, fontWeight: FontWeight.w600, fontSize: 13),
                  ),
                ],
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
              icon: const Icon(Icons.delete_sweep_rounded, color: Colors.redAccent),
              onPressed: _clearHistory,
            ),
        ],
      ),
      body: _history.isEmpty
          ? Center(
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: const Color(0xFF131B2E),
                      shape: BoxShape.circle,
                      border: Border.all(color: const Color(0xFF1E293B)),
                    ),
                    child: const Icon(Icons.history_rounded, size: 48, color: Color(0xFF64748B)),
                  ),
                  const SizedBox(height: 16),
                  const Text('No QR history yet', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 16, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 6),
                  const Text('Created & scanned codes will appear here', style: TextStyle(color: Color(0xFF64748B), fontSize: 13)),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              itemCount: _history.length,
              itemBuilder: (ctx, idx) {
                final item = _history[idx];
                final isCreated = item['type'] == 'Created';
                return Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  decoration: BoxDecoration(
                    color: const Color(0xFF131B2E),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: const Color(0xFF1E293B)),
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                    leading: Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: isCreated
                            ? const Color(0xFF4F46E5).withValues(alpha: 0.15)
                            : const Color(0xFF10B981).withValues(alpha: 0.15),
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Icon(
                        isCreated ? Icons.qr_code_2_rounded : Icons.qr_code_scanner_rounded,
                        color: isCreated ? const Color(0xFF818CF8) : const Color(0xFF34D399),
                        size: 22,
                      ),
                    ),
                    title: Text(
                      item['payload'] ?? '',
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14, color: Colors.white),
                    ),
                    subtitle: Text(
                      '${item['type']} • ${item['category'] ?? 'QR'}',
                      style: const TextStyle(fontSize: 12, color: Color(0xFF94A3B8)),
                    ),
                    trailing: IconButton(
                      icon: const Icon(Icons.copy_rounded, size: 18, color: Color(0xFF94A3B8)),
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
   4. ABOUT & PRIVACY SCREEN - Premium Settings Card
   ========================================================================= */
class AboutSettingsScreen extends StatelessWidget {
  const AboutSettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('About & Privacy')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Container(
              padding: const EdgeInsets.all(5),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(22),
                boxShadow: [
                  BoxShadow(color: const Color(0xFF6366F1).withValues(alpha: 0.25), blurRadius: 24, spreadRadius: 2),
                ],
              ),
              child: ClipRRect(
                borderRadius: BorderRadius.circular(18),
                child: Image.asset('assets/logo.png', width: 88, height: 88, fit: BoxFit.cover),
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'MyLogoQR',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800, color: Colors.white),
            ),
            const SizedBox(height: 4),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(99),
                border: Border.all(color: Colors.white12),
              ),
              child: const Text(
                'v1.1.0 • Native Android Edition',
                style: TextStyle(color: Color(0xFF94A3B8), fontSize: 11, fontWeight: FontWeight.w600),
              ),
            ),
            const SizedBox(height: 24),

            // Privacy Guarantee
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                color: const Color(0xFF131B2E),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFF1E293B)),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.verified_user_rounded, color: Color(0xFF10B981), size: 20),
                      SizedBox(width: 8),
                      Text('100% Client-Side Privacy Guarantee', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: Colors.white)),
                    ],
                  ),
                  SizedBox(height: 10),
                  Text(
                    'All barcodes, custom logos, and camera feeds are processed strictly in your device memory. Zero tracking, zero telemetry, and never sent to cloud servers.',
                    style: TextStyle(color: Color(0xFF94A3B8), fontSize: 13, height: 1.5),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),

            // Developer & Engineering Profile Card
            Container(
              decoration: BoxDecoration(
                color: const Color(0xFF131B2E),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: const Color(0xFF1E293B)),
              ),
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.fromLTRB(16, 16, 16, 12),
                    child: Row(
                      children: [
                        Container(
                          width: 44,
                          height: 44,
                          decoration: BoxDecoration(
                            gradient: const LinearGradient(
                              colors: [Color(0xFF6366F1), Color(0xFF8B5CF6)],
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                            ),
                            borderRadius: BorderRadius.circular(14),
                          ),
                          child: const Icon(Icons.person_outline_rounded, color: Colors.white, size: 24),
                        ),
                        const SizedBox(width: 14),
                        const Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Shahrukh Ahmad (SRK AMD)',
                                style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15, color: Colors.white),
                              ),
                              SizedBox(height: 2),
                              Text(
                                'Lead Engineer & Systems Architect',
                                style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Divider(color: Color(0xFF1E293B), height: 1),
                  ListTile(
                    leading: const Icon(Icons.language_rounded, color: Color(0xFF818CF8)),
                    title: const Text('Official Website', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white)),
                    subtitle: const Text('https://mylogoqr.com', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12)),
                    trailing: const Icon(Icons.open_in_new_rounded, size: 16, color: Color(0xFF64748B)),
                    onTap: () => launchUrl(Uri.parse('https://mylogoqr.com'), mode: LaunchMode.externalApplication),
                  ),
                  const Divider(color: Color(0xFF1E293B), height: 1),
                  ListTile(
                    leading: const Icon(Icons.code_rounded, color: Color(0xFF38BDF8)),
                    title: const Text('GitHub Profile', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white)),
                    subtitle: const Text('https://github.com/srkamd', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12)),
                    trailing: const Icon(Icons.open_in_new_rounded, size: 16, color: Color(0xFF64748B)),
                    onTap: () => launchUrl(Uri.parse('https://github.com/srkamd'), mode: LaunchMode.externalApplication),
                  ),
                  const Divider(color: Color(0xFF1E293B), height: 1),
                  ListTile(
                    leading: const Icon(Icons.star_rate_rounded, color: Colors.amber),
                    title: const Text('Rate on Google Play', style: TextStyle(fontWeight: FontWeight.w600, color: Colors.white)),
                    subtitle: const Text('com.mylogoqr.app', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 12)),
                    trailing: const Icon(Icons.open_in_new_rounded, size: 16, color: Color(0xFF64748B)),
                    onTap: () => launchUrl(
                      Uri.parse('https://play.google.com/store/apps/details?id=com.mylogoqr.app'),
                      mode: LaunchMode.externalApplication,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),
            const Text(
              'Engineered with ❤️ by Shahrukh Ahmad (SRK AMD)',
              style: TextStyle(color: Color(0xFF64748B), fontSize: 12, fontWeight: FontWeight.w500),
            ),
            const SizedBox(height: 4),
            const Text(
              '100% Free Forever • Zero Subscription Traps',
              style: TextStyle(color: Color(0xFF475569), fontSize: 11),
            ),
          ],
        ),
      ),
    );
  }
}
