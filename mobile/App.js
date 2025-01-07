import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from './src/screens/LoginScreen';
import HomeScreen from './src/screens/HomeScreen';
import ProgramDetailScreen from './src/screens/ProgramDetailScreen';
import WorkoutDetailScreen from './src/screens/WorkoutDetailScreen';

const Stack = createNativeStackNavigator();

const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator 
        initialRouteName="Login"
        screenOptions={{
          headerStyle: {
            backgroundColor: '#007AFF',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="Login" 
          component={LoginScreen} 
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Home" 
          component={HomeScreen}
          options={{
            title: 'Fitness App',
            headerLeft: () => null, // Disable back button
            gestureEnabled: false, // Disable swipe back gesture
          }}
        />
        <Stack.Screen 
          name="ProgramDetail" 
          component={ProgramDetailScreen}
          options={({ route }) => ({
            title: route.params.program.name,
          })}
        />
        <Stack.Screen 
          name="WorkoutDetail" 
          component={WorkoutDetailScreen}
          options={({ route }) => ({
            title: route.params.workout.name,
          })}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default App;
