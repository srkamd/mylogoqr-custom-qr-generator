import 'package:flutter_test/flutter_test.dart';
import 'package:app/main.dart';

void main() {
  testWidgets('MyLogoQR smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const MyLogoQRApp());
    expect(find.text('MyLogoQR'), findsWidgets);
  });
}
