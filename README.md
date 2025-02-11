# Fitness Application

A comprehensive fitness application with a Django backend and Flutter mobile frontend. This application helps users track their workouts, follow training programs, and connect with trainers.

## Project Structure

```
.
├── backend/         # Django backend application
│   ├── fitness_app/    # Main Django project
│   ├── messaging/      # Messaging and forum functionality
│   ├── nutrition/      # Nutrition tracking
│   ├── programs/       # Workout programs
│   ├── trainers/       # Trainer functionality
│   ├── users/          # User management
│   └── workouts/       # Workout and exercise management
│
└── mobile/          # Flutter mobile application
    ├── lib/            # Source code
    │   ├── models/     # Data models
    │   ├── screens/    # Screen widgets
    │   ├── services/   # API services
    │   └── widgets/    # Reusable widgets
    └── main.dart       # Entry point
```

## Backend (Django)

### Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

### Features

- User Authentication (Login/Register)
- Workout Program Management
- Exercise Library
- Trainer-Client Relationship
- Messaging System
- Nutrition Tracking
- Forum Discussions

## Mobile (Flutter)

### Setup

1. Install Flutter:
   - Follow the official Flutter installation guide: https://flutter.dev/docs/get-started/install

2. Install dependencies:
```bash
cd mobile
flutter pub get
```

3. Run the app:
```bash
flutter run
```

### Features

- User Authentication
- View and Track Workouts
- Follow Training Programs
- Connect with Trainers
- Track Nutrition
- Message Other Users

## API Integration

The Flutter mobile app communicates with the Django backend through RESTful APIs. The API endpoints are defined in the backend's URLs and consumed by the mobile app's services using the `http` package.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
