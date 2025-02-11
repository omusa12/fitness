import 'package:flutter_test/flutter_test.dart';
import 'package:fitness_app/main.dart';
import 'package:fitness_app/services/auth_service.dart';
import 'package:fitness_app/services/client_service.dart';
import 'package:fitness_app/services/notification_service.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    // Create mock services
    final authService = AuthService();
    final clientService = ClientService(baseUrl: 'http://localhost:8000');
    final notificationService = NotificationService();

    // Build our app and trigger a frame
    await tester.pumpWidget(MyApp(
      authService: authService,
      clientService: clientService,
      notificationService: notificationService,
    ));

    // Verify that the splash screen is shown initially
    expect(find.text('Fitness App'), findsOneWidget);
  });
}
