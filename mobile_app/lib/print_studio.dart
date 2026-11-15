import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'package:path_provider/path_provider.dart';
import 'package:share_plus/share_plus.dart';

class PrintStudioScreen extends StatefulWidget {
  final Uint8List qrBytes;
  final String currentType;
  final String initialHeadline;
  final String initialSubtext;

  const PrintStudioScreen({
    super.key,
    required this.qrBytes,
    required this.currentType,
    required this.initialHeadline,
    required this.initialSubtext,
  });

  @override
  State<PrintStudioScreen> createState() => _PrintStudioScreenState();
}

class _PrintStudioScreenState extends State<PrintStudioScreen> {
  String _preset = 'standee'; // standee, table, wifi, review, stickers12, businesscard, flyer
  late TextEditingController _headerController;
  late TextEditingController _subController;

  String _paper = 'A4'; // A4, Letter, A5, A6
  String _colorMode = 'brand'; // brand, mono, cmyk
  Color _accentColor = const Color(0xFF4F46E5);
  bool _cropMarks = true;
  bool _safeZone = true;
  bool _isGenerating = false;

  final List<Color> _accentColors = const [
    Color(0xFF4F46E5), // Indigo
    Color(0xFF059669), // Emerald
    Color(0xFF0284C7), // Sky Blue
    Color(0xFFDC2626), // Crimson
    Color(0xFFD97706), // Amber
    Color(0xFF0F172A), // Jet Black
  ];

  @override
  void initState() {
    super.initState();
    _headerController = TextEditingController(text: widget.initialHeadline);
    _subController = TextEditingController(text: widget.initialSubtext);
    if (widget.currentType == 'Wi-Fi') {
      _preset = 'wifi';
      _accentColor = const Color(0xFF0284C7);
    } else if (widget.currentType == 'vCard') {
      _preset = 'businesscard';
      _accentColor = const Color(0xFF0F172A);
    }
  }

  @override
  void dispose() {
    _headerController.dispose();
    _subController.dispose();
    super.dispose();
  }

  void _onPresetChanged(String newPreset) {
    setState(() {
      _preset = newPreset;
      if (newPreset == 'wifi') {
        _headerController.text = 'Free Guest Wi-Fi';
        _subController.text = 'Scan with camera to connect automatically';
        _accentColor = const Color(0xFF0284C7);
      } else if (newPreset == 'review') {
        _headerController.text = 'Review Us On Google';
        _subController.text = 'Loved your experience? Scan to leave a 5-star review!';
        _accentColor = const Color(0xFFD97706);
      } else if (newPreset == 'table') {
        _headerController.text = 'Digital Menu & Ordering';
        _subController.text = 'Scan from table to browse food & drinks menu';
        _accentColor = const Color(0xFFDC2626);
      } else if (newPreset == 'businesscard') {
        _headerController.text = 'Digital Business Card';
        _subController.text = 'Scan with phone camera to save full contact details.';
        _accentColor = const Color(0xFF0F172A);
      } else if (newPreset == 'stickers12') {
        _headerController.text = 'SCAN ME';
        _subController.text = '';
      } else {
        _headerController.text = 'Scan To Connect';
        _subController.text = 'Point your phone camera to scan instantly';
        _accentColor = const Color(0xFF4F46E5);
      }
    });
  }

  PdfColor _getPdfAccentColor() {
    if (_colorMode == 'mono') return PdfColors.black;
    if (_colorMode == 'cmyk') return const PdfColor(0.07, 0.09, 0.15);
    return PdfColor(
      _accentColor.r,
      _accentColor.g,
      _accentColor.b,
    );
  }

  PdfPageFormat _getPdfPageFormat() {
    switch (_paper) {
      case 'Letter':
        return PdfPageFormat.letter;
      case 'A5':
        return PdfPageFormat.a5;
      case 'A6':
        return PdfPageFormat.a6;
      case 'A4':
      default:
        return PdfPageFormat.a4;
    }
  }

  Future<Uint8List> _generatePdfDocument() async {
    final pdf = pw.Document();
    final format = _getPdfPageFormat();
    final qrImage = pw.MemoryImage(widget.qrBytes);
    final pdfAccent = _getPdfAccentColor();
    final headline = _headerController.text.trim().isEmpty ? 'Scan To Connect' : _headerController.text.trim();
    final subtext = _subController.text.trim();

    if (_preset == 'stickers12') {
      // 12 Stickers on 1 Sheet (Grid 3x4)
      pdf.addPage(
        pw.Page(
          pageFormat: format,
          margin: const pw.EdgeInsets.all(20),
          build: (pw.Context context) {
            return pw.GridView(
              crossAxisCount: 3,
              childAspectRatio: 0.85,
              children: List.generate(12, (index) {
                return pw.Container(
                  margin: const pw.EdgeInsets.all(6),
                  padding: const pw.EdgeInsets.all(10),
                  decoration: pw.BoxDecoration(
                    border: pw.Border.all(color: PdfColors.grey300, width: 1, style: pw.BorderStyle.dashed),
                    borderRadius: pw.BorderRadius.circular(8),
                  ),
                  child: pw.Column(
                    mainAxisAlignment: pw.MainAxisAlignment.center,
                    children: [
                      pw.Container(
                        width: 90,
                        height: 90,
                        child: pw.Image(qrImage),
                      ),
                      pw.SizedBox(height: 6),
                      pw.Text(
                        headline,
                        style: pw.TextStyle(
                          color: pdfAccent,
                          fontWeight: pw.FontWeight.bold,
                          fontSize: 10,
                        ),
                        textAlign: pw.TextAlign.center,
                      ),
                    ],
                  ),
                );
              }),
            );
          },
        ),
      );
    } else if (_preset == 'businesscard') {
      // Standard Business Card (3.5" x 2")
      pdf.addPage(
        pw.Page(
          pageFormat: const PdfPageFormat(3.5 * PdfPageFormat.inch, 2.0 * PdfPageFormat.inch, marginAll: 0.2 * PdfPageFormat.inch),
          build: (pw.Context context) {
            return pw.Container(
              decoration: pw.BoxDecoration(
                border: pw.Border.all(color: pdfAccent, width: 1),
                borderRadius: pw.BorderRadius.circular(6),
              ),
              padding: const pw.EdgeInsets.all(12),
              child: pw.Row(
                crossAxisAlignment: pw.CrossAxisAlignment.center,
                mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                children: [
                  pw.Expanded(
                    child: pw.Column(
                      crossAxisAlignment: pw.CrossAxisAlignment.start,
                      mainAxisAlignment: pw.MainAxisAlignment.center,
                      children: [
                        pw.Text(
                          headline,
                          style: pw.TextStyle(color: pdfAccent, fontWeight: pw.FontWeight.bold, fontSize: 13),
                        ),
                        pw.SizedBox(height: 4),
                        pw.Text(
                          subtext,
                          style: const pw.TextStyle(color: PdfColors.grey700, fontSize: 8),
                        ),
                        pw.SizedBox(height: 8),
                        pw.Text(
                          'Direct Scan & Save',
                          style: const pw.TextStyle(color: PdfColors.grey500, fontSize: 7),
                        ),
                      ],
                    ),
                  ),
                  pw.SizedBox(width: 8),
                  pw.Container(
                    width: 75,
                    height: 75,
                    child: pw.Image(qrImage),
                  ),
                ],
              ),
            );
          },
        ),
      );
    } else {
      // Standee, Table Tent, Wi-Fi Sign, Review Card, Flyer
      pdf.addPage(
        pw.Page(
          pageFormat: format,
          margin: const pw.EdgeInsets.all(36),
          build: (pw.Context context) {
            String badgeText = 'TABLE / COUNTER DISPLAY';
            if (_preset == 'wifi') badgeText = 'HIGH-SPEED GUEST WI-FI';
            if (_preset == 'review') badgeText = 'FIVE STAR GOOGLE REVIEWS';
            if (_preset == 'table') badgeText = 'TABLE TENT &bull; DINE IN';
            if (_preset == 'flyer') badgeText = 'OFFICIAL QR NOTICE';

            return pw.Center(
              child: pw.Container(
                width: 380,
                padding: const pw.EdgeInsets.all(32),
                decoration: pw.BoxDecoration(
                  border: pw.Border.all(
                    color: pdfAccent,
                    width: _preset == 'table' ? 2 : 1.5,
                    style: _preset == 'table' ? pw.BorderStyle.dashed : pw.BorderStyle.solid,
                  ),
                  borderRadius: pw.BorderRadius.circular(16),
                ),
                child: pw.Column(
                  mainAxisSize: pw.MainAxisSize.min,
                  crossAxisAlignment: pw.CrossAxisAlignment.center,
                  children: [
                    // Badge
                    pw.Container(
                      padding: const pw.EdgeInsets.symmetric(horizontal: 14, vertical: 5),
                      decoration: pw.BoxDecoration(
                        color: _colorMode == 'mono' ? PdfColors.grey200 : const PdfColor(0.93, 0.94, 0.99),
                        borderRadius: pw.BorderRadius.circular(20),
                      ),
                      child: pw.Text(
                        badgeText,
                        style: pw.TextStyle(
                          color: pdfAccent,
                          fontWeight: pw.FontWeight.bold,
                          fontSize: 9,
                          letterSpacing: 0.5,
                        ),
                      ),
                    ),
                    pw.SizedBox(height: 16),

                    // Headline
                    pw.Text(
                      headline,
                      style: pw.TextStyle(
                        color: _colorMode == 'mono' ? PdfColors.black : const PdfColor(0.06, 0.09, 0.16),
                        fontWeight: pw.FontWeight.bold,
                        fontSize: 20,
                      ),
                      textAlign: pw.TextAlign.center,
                    ),
                    pw.SizedBox(height: 6),

                    // Subtext
                    if (subtext.isNotEmpty)
                      pw.Text(
                        subtext,
                        style: const pw.TextStyle(color: PdfColors.grey700, fontSize: 11),
                        textAlign: pw.TextAlign.center,
                      ),
                    pw.SizedBox(height: 24),

                    // QR Frame
                    pw.Container(
                      padding: pw.EdgeInsets.all(_safeZone ? 16 : 6),
                      decoration: pw.BoxDecoration(
                        border: pw.Border.all(color: PdfColors.grey300, width: 1.5),
                        borderRadius: pw.BorderRadius.circular(14),
                      ),
                      child: pw.Container(
                        width: 170,
                        height: 170,
                        child: pw.Image(qrImage),
                      ),
                    ),
                    pw.SizedBox(height: 24),

                    // Footer
                    pw.Text(
                      'Free & Private • Powered by MyLogoQR',
                      style: const pw.TextStyle(color: PdfColors.grey500, fontSize: 9),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      );
    }

    return pdf.save();
  }

  Future<void> _handleDirectPrint() async {
    setState(() => _isGenerating = true);
    try {
      final bytes = await _generatePdfDocument();
      await Printing.layoutPdf(
        onLayout: (PdfPageFormat format) async => bytes,
        name: 'MyLogoQR_Print_Template.pdf',
      );
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Print failed: $e')));
      }
    } finally {
      if (mounted) setState(() => _isGenerating = false);
    }
  }

  Future<void> _handleSharePdf() async {
    setState(() => _isGenerating = true);
    try {
      final bytes = await _generatePdfDocument();
      final tempDir = await getTemporaryDirectory();
      final file = File('${tempDir.path}/MyLogoQR_Print_${DateTime.now().millisecondsSinceEpoch}.pdf');
      await file.writeAsBytes(bytes);
      await Share.shareXFiles([XFile(file.path)], text: 'MyLogoQR Printable PDF Template');
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Share failed: $e')));
      }
    } finally {
      if (mounted) setState(() => _isGenerating = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF090D16),
      appBar: AppBar(
        title: const Text('Professional Print & PDF Studio', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 17)),
        leading: IconButton(
          icon: const Icon(Icons.close_rounded),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Preview Card
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: _colorMode == 'mono' ? Colors.black : _accentColor,
                  width: _preset == 'table' ? 2 : 1.5,
                ),
                boxShadow: [
                  BoxShadow(color: Colors.black.withValues(alpha: 0.25), blurRadius: 16, offset: const Offset(0, 4)),
                ],
              ),
              child: _buildLiveVisualPreview(),
            ),
            const SizedBox(height: 20),

            // Controls Card
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
                  const Text('1. Physical Print Format', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: Colors.white)),
                  const SizedBox(height: 8),
                  _buildDropdown<String>(
                    value: _preset,
                    items: const [
                      DropdownMenuItem(value: 'standee', child: Text('Acrylic Standee / Counter Display')),
                      DropdownMenuItem(value: 'table', child: Text('Table Tent / Cafe Menu (Dine-In)')),
                      DropdownMenuItem(value: 'wifi', child: Text('High-Speed Wi-Fi Guest Board')),
                      DropdownMenuItem(value: 'review', child: Text('Google 5-Star Review Standee')),
                      DropdownMenuItem(value: 'stickers12', child: Text('12-Sticker Sheet (A4 / Letter 3x4 Grid)')),
                      DropdownMenuItem(value: 'businesscard', child: Text('Standard Business Card (3.5" x 2")')),
                      DropdownMenuItem(value: 'flyer', child: Text('Full Page Poster / Notice (A4/Letter)')),
                    ],
                    onChanged: (val) => val != null ? _onPresetChanged(val) : null,
                  ),
                  const SizedBox(height: 16),

                  // Headline & Subtext
                  const Text('2. Signage Headline', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: Colors.white)),
                  const SizedBox(height: 8),
                  TextField(
                    controller: _headerController,
                    style: const TextStyle(color: Colors.white, fontSize: 14),
                    onChanged: (_) => setState(() {}),
                    decoration: InputDecoration(
                      hintText: 'e.g. Scan To Connect',
                      hintStyle: const TextStyle(color: Color(0xFF64748B)),
                      filled: true,
                      fillColor: const Color(0xFF0B0F19),
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF1E293B))),
                    ),
                  ),
                  const SizedBox(height: 12),

                  if (_preset != 'stickers12') ...[
                    const Text('Instructions / Subtext', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: Colors.white)),
                    const SizedBox(height: 8),
                    TextField(
                      controller: _subController,
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                      onChanged: (_) => setState(() {}),
                      decoration: InputDecoration(
                        hintText: 'e.g. Point phone camera to scan instantly',
                        hintStyle: const TextStyle(color: Color(0xFF64748B)),
                        filled: true,
                        fillColor: const Color(0xFF0B0F19),
                        border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: const BorderSide(color: Color(0xFF1E293B))),
                      ),
                    ),
                    const SizedBox(height: 16),
                  ],

                  // Paper standard & Color mode
                  Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Paper Size', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13, color: Colors.white)),
                            const SizedBox(height: 6),
                            _buildDropdown<String>(
                              value: _paper,
                              items: const [
                                DropdownMenuItem(value: 'A4', child: Text('A4 (Global)')),
                                DropdownMenuItem(value: 'Letter', child: Text('Letter (US)')),
                                DropdownMenuItem(value: 'A5', child: Text('A5 (Flyer)')),
                                DropdownMenuItem(value: 'A6', child: Text('A6 (Card)')),
                              ],
                              onChanged: (v) => v != null ? setState(() => _paper = v) : null,
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Color Mode', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13, color: Colors.white)),
                            const SizedBox(height: 6),
                            _buildDropdown<String>(
                              value: _colorMode,
                              items: const [
                                DropdownMenuItem(value: 'brand', child: Text('Color Brand')),
                                DropdownMenuItem(value: 'mono', child: Text('100% Black')),
                                DropdownMenuItem(value: 'cmyk', child: Text('Charcoal CMYK')),
                              ],
                              onChanged: (v) => v != null ? setState(() => _colorMode = v) : null,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Accent Colors
                  if (_colorMode == 'brand') ...[
                    const Text('Theme Accent Color', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 13, color: Colors.white)),
                    const SizedBox(height: 8),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: _accentColors.map((c) {
                        final isSel = _accentColor == c;
                        return GestureDetector(
                          onTap: () => setState(() => _accentColor = c),
                          child: Container(
                            width: 38,
                            height: 38,
                            decoration: BoxDecoration(
                              color: c,
                              shape: BoxShape.circle,
                              border: Border.all(color: isSel ? Colors.white : Colors.transparent, width: 2.5),
                              boxShadow: isSel ? [BoxShadow(color: c.withValues(alpha: 0.6), blurRadius: 10)] : null,
                            ),
                            child: isSel ? const Icon(Icons.check, size: 20, color: Colors.white) : null,
                          ),
                        );
                      }).toList(),
                    ),
                    const SizedBox(height: 16),
                  ],

                  // Checkboxes
                  SwitchListTile(
                    contentPadding: EdgeInsets.zero,
                    title: const Text('Corner Cutting & Trim Marks', style: TextStyle(fontSize: 13, color: Colors.white, fontWeight: FontWeight.w600)),
                    subtitle: const Text('Guides for cutting cleanly with scissors or trimmer', style: TextStyle(fontSize: 11, color: Color(0xFF64748B))),
                    value: _cropMarks,
                    activeThumbColor: const Color(0xFF6366F1),
                    onChanged: (v) => setState(() => _cropMarks = v),
                  ),
                  SwitchListTile(
                    contentPadding: EdgeInsets.zero,
                    title: const Text('Enforce Camera Quiet-Zone Margin', style: TextStyle(fontSize: 13, color: Colors.white, fontWeight: FontWeight.w600)),
                    subtitle: const Text('Protects QR corners from physical clipping', style: TextStyle(fontSize: 11, color: Color(0xFF64748B))),
                    value: _safeZone,
                    activeThumbColor: const Color(0xFF6366F1),
                    onChanged: (v) => setState(() => _safeZone = v),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Print & Export Buttons
            Container(
              width: double.infinity,
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [Color(0xFF4F46E5), Color(0xFF3730A3)]),
                borderRadius: BorderRadius.circular(16),
                boxShadow: [
                  BoxShadow(color: const Color(0xFF4F46E5).withValues(alpha: 0.4), blurRadius: 16, offset: const Offset(0, 6)),
                ],
              ),
              child: ElevatedButton.icon(
                onPressed: _isGenerating ? null : _handleDirectPrint,
                icon: _isGenerating
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                    : const Icon(Icons.print_rounded, size: 22),
                label: const Text('🖨️ Direct Print / Save as PDF', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.transparent,
                  shadowColor: Colors.transparent,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                ),
              ),
            ),
            const SizedBox(height: 10),

            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: _isGenerating ? null : _handleSharePdf,
                icon: const Icon(Icons.share_rounded, size: 20, color: Color(0xFF818CF8)),
                label: const Text('Share PDF File (WhatsApp / Drive)', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15, color: Colors.white)),
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: Color(0xFF312E81), width: 1.5),
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                ),
              ),
            ),
            const SizedBox(height: 32),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdown<T>({required T value, required List<DropdownMenuItem<T>> items, required ValueChanged<T?> onChanged}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
      decoration: BoxDecoration(
        color: const Color(0xFF0B0F19),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF1E293B)),
      ),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<T>(
          value: value,
          isExpanded: true,
          dropdownColor: const Color(0xFF131B2E),
          style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w500),
          items: items,
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _buildLiveVisualPreview() {
    final activeColor = _colorMode == 'mono' ? Colors.black : _accentColor;
    final headline = _headerController.text.trim().isEmpty ? 'Scan To Connect' : _headerController.text.trim();
    final subtext = _subController.text.trim();

    if (_preset == 'stickers12') {
      return GridView.builder(
        shrinkWrap: true,
        physics: const NeverScrollableScrollPhysics(),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 3,
          childAspectRatio: 0.9,
          crossAxisSpacing: 8,
          mainAxisSpacing: 8,
        ),
        itemCount: 6, // Show 6 sample stickers on mobile screen preview
        itemBuilder: (context, i) {
          return Container(
            decoration: BoxDecoration(
              border: Border.all(color: activeColor.withValues(alpha: 0.4), style: BorderStyle.solid),
              borderRadius: BorderRadius.circular(8),
            ),
            padding: const EdgeInsets.all(6),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Expanded(child: Image.memory(widget.qrBytes, fit: BoxFit.contain)),
                const SizedBox(height: 2),
                Text(headline, style: TextStyle(color: activeColor, fontWeight: FontWeight.bold, fontSize: 8), maxLines: 1),
              ],
            ),
          );
        },
      );
    }

    if (_preset == 'businesscard') {
      return Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(headline, style: TextStyle(color: activeColor, fontWeight: FontWeight.w900, fontSize: 16)),
                const SizedBox(height: 4),
                Text(subtext, style: const TextStyle(color: Color(0xFF475569), fontSize: 11)),
                const SizedBox(height: 8),
                const Text('Instant Contact Save', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 9, fontWeight: FontWeight.w600)),
              ],
            ),
          ),
          const SizedBox(width: 14),
          Container(
            width: 90,
            height: 90,
            decoration: BoxDecoration(
              border: Border.all(color: const Color(0xFFE2E8F0)),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Image.memory(widget.qrBytes),
          ),
        ],
      );
    }

    return Column(
      mainAxisSize: MainAxisSize.min,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          decoration: BoxDecoration(
            color: activeColor.withValues(alpha: 0.1),
            borderRadius: BorderRadius.circular(99),
          ),
          child: Text(
            _preset == 'wifi' ? 'HIGH-SPEED GUEST WI-FI' : (_preset == 'review' ? '★ ★ ★ ★ ★ FIVE STARS' : 'TABLE & COUNTER DISPLAY'),
            style: TextStyle(color: activeColor, fontWeight: FontWeight.w800, fontSize: 10, letterSpacing: 0.5),
          ),
        ),
        const SizedBox(height: 12),
        Text(
          headline,
          style: const TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.w900, fontSize: 18),
          textAlign: TextAlign.center,
        ),
        if (subtext.isNotEmpty) ...[
          const SizedBox(height: 4),
          Text(subtext, style: const TextStyle(color: Color(0xFF64748B), fontSize: 12), textAlign: TextAlign.center),
        ],
        const SizedBox(height: 16),
        Container(
          padding: EdgeInsets.all(_safeZone ? 12 : 4),
          decoration: BoxDecoration(
            border: Border.all(color: const Color(0xFFCBD5E1), width: 1.5),
            borderRadius: BorderRadius.circular(14),
          ),
          child: SizedBox(
            width: 150,
            height: 150,
            child: Image.memory(widget.qrBytes),
          ),
        ),
        const SizedBox(height: 12),
        const Text('Powered by MyLogoQR • Ready for Print', style: TextStyle(color: Color(0xFF94A3B8), fontSize: 10, fontWeight: FontWeight.w600)),
      ],
    );
  }
}
