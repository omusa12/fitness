import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';

const ProgramDetailScreen = ({ route, navigation }) => {
  const { program } = route.params;

  const renderWorkout = (workout) => (
    <TouchableOpacity
      key={workout.id}
      style={styles.workoutCard}
      onPress={() => navigation.navigate('WorkoutDetail', { workout })}
    >
      <Text style={styles.workoutTitle}>{workout.name}</Text>
      <View style={styles.workoutInfo}>
        <Text style={styles.workoutDetail}>
          Exercises: {workout.exercises?.length || 0}
        </Text>
        <Text style={styles.workoutDetail}>
          Duration: {workout.duration || 'Not specified'}
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{program.name}</Text>
        <Text style={styles.description}>{program.description}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Program Details</Text>
        <View style={styles.detailsContainer}>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Duration:</Text>
            <Text style={styles.detailValue}>
              {program.duration || 'Not specified'}
            </Text>
          </View>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Difficulty:</Text>
            <Text style={styles.detailValue}>
              {program.difficulty || 'Not specified'}
            </Text>
          </View>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Workouts</Text>
        {program.workouts && program.workouts.length > 0 ? (
          program.workouts.map(renderWorkout)
        ) : (
          <Text style={styles.emptyText}>No workouts in this program</Text>
        )}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  header: {
    padding: 20,
    backgroundColor: '#007AFF',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 10,
  },
  description: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  detailsContainer: {
    backgroundColor: '#f5f5f5',
    borderRadius: 10,
    padding: 15,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  detailLabel: {
    fontSize: 16,
    color: '#666',
  },
  detailValue: {
    fontSize: 16,
    fontWeight: '500',
  },
  workoutCard: {
    backgroundColor: '#f5f5f5',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
  },
  workoutTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  workoutInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  workoutDetail: {
    fontSize: 14,
    color: '#666',
  },
  emptyText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#666',
    marginTop: 20,
  },
});

export default ProgramDetailScreen;
