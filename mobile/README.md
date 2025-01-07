# FitnessApp Mobile

React Native mobile application for the Fitness App platform. This app connects to a Django backend to provide a seamless fitness tracking experience.

## Features

- User authentication
- View fitness programs
- Program details with associated workouts
- Detailed workout information with exercises
- Pull-to-refresh data updates

## Prerequisites

- Node.js
- npm or yarn
- React Native development environment setup
- Android Studio (for Android development)
- XCode (for iOS development)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fitness-app-mobile.git
cd fitness-app-mobile
```

2. Install dependencies:
```bash
npm install
```

3. Update the API endpoint:
In `src/services/api.js`, update the `baseURL` to point to your Django backend server.

## Running the App

1. Start the Metro bundler:
```bash
npm start
```

2. Run on Android:
```bash
npm run android
```

3. Run on iOS:
```bash
npm run ios
```

## Project Structure

```
src/
  ├── screens/          # Screen components
  │   ├── LoginScreen.js
  │   ├── HomeScreen.js
  │   ├── ProgramDetailScreen.js
  │   └── WorkoutDetailScreen.js
  └── services/         # API and other services
      └── api.js
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
