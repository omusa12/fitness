from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TrainerWorkout
from programs.models import ProgramWorkout
from .serializers import TrainerWorkoutSerializer, ProgramWorkoutSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_workouts_list(request):
    """API endpoint to get list of workouts for the authenticated user."""
    if request.user.is_trainer:
        # For trainers, return their created workout templates
        workouts = TrainerWorkout.objects.filter(trainer=request.user)
        serializer = TrainerWorkoutSerializer(workouts, many=True)
    else:
        # For clients, return workouts from their assigned programs
        workouts = ProgramWorkout.objects.filter(
            program__client=request.user,
            program__is_active=True
        )
        serializer = ProgramWorkoutSerializer(workouts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_workout_detail(request, pk):
    """API endpoint to get details of a specific workout."""
    try:
        if request.user.is_trainer:
            workout = TrainerWorkout.objects.get(pk=pk, trainer=request.user)
            serializer = TrainerWorkoutSerializer(workout)
        else:
            workout = ProgramWorkout.objects.get(
                pk=pk,
                program__client=request.user,
                program__is_active=True
            )
            serializer = ProgramWorkoutSerializer(workout)
        return Response(serializer.data)
    except (TrainerWorkout.DoesNotExist, ProgramWorkout.DoesNotExist):
        return Response(
            {"error": "Workout not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
