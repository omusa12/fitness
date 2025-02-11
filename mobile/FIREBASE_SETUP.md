# Firebase Setup Guide

This guide explains how to set up Firebase for the Fitness App's authentication system.

## Prerequisites

1. A Google account
2. [Firebase Console](https://console.firebase.google.com/) access
3. Flutter development environment set up

## Setup Steps

### 1. Create Firebase Project

1. Go to the [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Enter "Fitness App" as the project name
4. Follow the setup wizard (enable Google Analytics if desired)

### 2. Android Setup

1. In the Firebase Console, click "Add App" and select Android
2. Enter the package name: `com.example.fitness_app` (or your actual package name)
3. Download the `google-services.json` file
4. Place it in `android/app/google-services.json`
5. Update `android/build.gradle`:
```gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.3.15'
    }
}
```
6. Update `android/app/build.gradle`:
```gradle
apply plugin: 'com.google.gms.google-services'

dependencies {
    implementation platform('com.google.firebase:firebase-bom:32.2.0')
}
```

### 3. iOS Setup

1. In the Firebase Console, click "Add App" and select iOS
2. Enter your bundle ID (found in Xcode)
3. Download the `GoogleService-Info.plist` file
4. Place it in `ios/Runner/GoogleService-Info.plist`
5. Update `ios/Podfile`:
```ruby
platform :ios, '12.0'
```
6. Run `pod install` in the `ios` directory

### 4. Update Firebase Options

1. Copy the configuration values from your Firebase project settings
2. Update `lib/firebase_options.dart` with your values:
```dart
static const FirebaseOptions android = FirebaseOptions(
  apiKey: 'your-api-key',
  appId: 'your-app-id',
  messagingSenderId: 'your-sender-id',
  projectId: 'your-project-id',
  storageBucket: 'your-storage-bucket',
);

static const FirebaseOptions ios = FirebaseOptions(
  apiKey: 'your-api-key',
  appId: 'your-app-id',
  messagingSenderId: 'your-sender-id',
  projectId: 'your-project-id',
  storageBucket: 'your-storage-bucket',
  iosClientId: 'your-ios-client-id',
  iosBundleId: 'your-bundle-id',
);
```

### 5. Enable Authentication Methods

1. In the Firebase Console, go to Authentication
2. Click "Get Started"
3. Enable the following providers:
   - Email/Password
   - Google Sign-In
   - Apple Sign-In (for iOS)

### 6. Configure OAuth

#### Google Sign-In
1. In the Firebase Console, go to Authentication > Sign-in method
2. Enable Google Sign-In
3. Add your SHA-1 fingerprint for Android:
```bash
cd android
./gradlew signingReport
```

#### Apple Sign-In (iOS only)
1. Set up Apple Sign-In in your Apple Developer account
2. Configure Sign in with Apple in Xcode
3. Add the required capabilities in Xcode:
   - Sign In with Apple
   - Push Notifications

## Testing

1. Run the app in debug mode
2. Try signing in with each method:
   - Email/Password
   - Google
   - Apple (iOS only)
3. Verify that user data is being stored in Firebase

## Common Issues

### Android
- If Google Sign-In fails, verify your SHA-1 fingerprint is correct
- Ensure `google-services.json` is in the correct location
- Check Android package name matches Firebase configuration

### iOS
- Verify Bundle ID matches Firebase configuration
- Ensure `GoogleService-Info.plist` is included in the Xcode project
- Check that all required capabilities are enabled in Xcode

## Security Rules

Update Firebase Security Rules to protect user data:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

## Environment Variables

Consider using environment variables for sensitive Firebase configuration:

1. Create `.env` file (add to .gitignore):
```
FIREBASE_API_KEY=your-api-key
FIREBASE_APP_ID=your-app-id
```

2. Use [flutter_dotenv](https://pub.dev/packages/flutter_dotenv) to load variables:
```dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

await dotenv.load(fileName: ".env");
String apiKey = dotenv.env['FIREBASE_API_KEY']!;
```

## Next Steps

1. Implement proper error handling for authentication failures
2. Add user profile management
3. Set up Firebase Analytics for tracking user behavior
4. Configure Firebase Cloud Messaging for push notifications
5. Add Firebase Crashlytics for crash reporting

## Resources

- [Firebase Flutter Documentation](https://firebase.flutter.dev/docs/overview/)
- [FlutterFire CLI](https://firebase.flutter.dev/docs/cli/)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
- [Firebase Authentication](https://firebase.google.com/docs/auth)