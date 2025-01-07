import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';

const WorkoutDetailScreen = ({ route }) => {
  const { workout } = route.params;

  const renderExercise = (exercise, index) => (
    <View key={exercise.id} style={styles.exerciseCard}>
      <View style={styles.exerciseHeader}>
        <Text style={styles.exerciseTitle}>
          {index + 1}. {exercise.name}
        </Text>
      </View>
      <View style={styles.exerciseDetails}>
        {exercise.sets && (
          <View style={styles.detailItem}>
            <Text style={styles.detailLabel}>Sets:</Text>
            <Text style={styles.detailValue}>{exercise.sets}</Text>
          </View>
        )}
        {exercise.reps && (
          <View style={styles.detailItem}>
            <Text style={styles.detailLabel}>Reps:</Text>
            <Text style={styles.detailValue}>{exercise.reps}</Text>
          </View>
        )}
        {exercise.duration && (
          <View style={styles.detailItem}>
            <Text style={styles.detailLabel}>Duration:</Text>
            <Text style={styles.detailValue}>{exercise.duration}</Text>
          </View>
        )}
        {exercise.rest && (
          <View style={styles.detailItem}>
            <Text style={styles.detailLabel}>Rest:</Text>
            <Text style={styles.detailValue}>{exercise.rest}</Text>
          </View>
        )}
      </View>
      {exercise.notes && (
        <Text style={styles.exerciseNotes}>Notes: {exercise.notes}</Text>
      )}
    </View>
  );

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{workout.name}</Text>
        {workout.description && (
          <Text style={styles.description}>{workout.description}</Text>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Workout Details</Text>
        <View style={styles.detailsContainer}>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Duration:</Text>
            <Text style={styles.detailValue}>
              {workout.duration || 'Not specified'}
            </Text>
          </View>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Difficulty:</Text>
            <Text style={styles.detailValue}>
              {workout.difficulty || 'Not specified'}
            </Text>
          </View>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Exercises</Text>
        {workout.exercises && workout.exercises.length > 0 ? (
          workout.exercises.map((exercise, index) => 
            renderExercise(exercise, index)
          )
        ) : (
          <Text style={styles.emptyText}>No exercises in this workout</Text>
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
  exerciseCard: {
    backgroundColor: '#f5f5f5',
    borderRadius: 10,
    padding: 15,
    marginBottom: 15,
  },
  exerciseHeader: {
    marginBottom: 10,
  },
  exerciseTitle: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  exerciseDetails: {
    marginBottom: 10,
  },
  detailItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 5,
  },
  exerciseNotes: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
  },
  emptyText: {
    textAlign: 'center',
    fontSize: 16,
    color: '#666',
    marginTop: 20,
  },
});

export default WorkoutDetailScreen;
