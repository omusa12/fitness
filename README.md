# Fitness Application

A comprehensive fitness application with a Django backend and React Native mobile frontend. This application helps users track their workouts, follow training programs, and connect with trainers.

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
└── mobile/          # React Native mobile application
    ├── src/            # Source code
    │   ├── screens/    # Screen components
    │   └── services/   # API services
    └── App.js          # Root component
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

## Mobile (React Native)

### Setup

1. Install dependencies:
```bash
cd mobile
npm install
```

2. Start the development server:
```bash
npm start
```

3. Run on iOS/Android:
```bash
# iOS
npx pod-install ios
npm run ios

# Android
npm run android
```

### Features

- User Authentication
- View and Track Workouts
- Follow Training Programs
- Connect with Trainers
- Track Nutrition
- Message Other Users

## API Integration

The mobile app communicates with the Django backend through RESTful APIs. The API endpoints are defined in the backend's URLs and consumed by the mobile app's services.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
