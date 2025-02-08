from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Program
from .serializers import ProgramSerializer, CalendarEventSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_programs_list(request):
    """API endpoint to get list of programs for the authenticated user."""
    if request.user.is_trainer:
        # For trainers, return programs they created
        programs = Program.objects.filter(trainer=request.user)
    else:
        # For clients, return programs assigned to them
        programs = Program.objects.filter(client=request.user, is_active=True)
    
    serializer = ProgramSerializer(programs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_program_detail(request, pk):
    """API endpoint to get details of a specific program."""
    try:
        if request.user.is_trainer:
            program = Program.objects.get(pk=pk, trainer=request.user)
        else:
            program = Program.objects.get(pk=pk, client=request.user, is_active=True)
        
        serializer = ProgramSerializer(program)
        return Response(serializer.data)
    except Program.DoesNotExist:
        return Response(
            {"error": "Program not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_calendar_events(request):
    """API endpoint to get workout events for the calendar."""
    print(f"\nCalendar API - User: {request.user.username} (Trainer: {request.user.is_trainer})")
    
    if request.user.is_trainer:
        programs = Program.objects.filter(trainer=request.user, is_active=True)
    else:
        programs = Program.objects.filter(client=request.user, is_active=True)
    
    print(f"Found {programs.count()} active programs")
    
    events = []
    today = datetime.now().date()
    print(f"Today's date: {today}")
    
    for program in programs:
        print(f"\nProcessing program: {program.name}")
        if not program.start_date:
            print(f"- Skipping: No start date")
            continue
            
        # Calculate dates for the program duration
        program_end = program.start_date + timedelta(weeks=program.number_of_weeks)
        if program_end < today:
            print(f"- Skipping: Program ended ({program_end})")
            continue
            
        current_date = max(program.start_date, today)
        print(f"- Date range: {current_date} to {program_end}")
        
        while current_date <= program_end:
            # Get workouts scheduled for this day of the week
            day_workouts = program.workouts.filter(day_of_week=current_date.weekday())
            
            if day_workouts.exists():
                print(f"- Found {day_workouts.count()} workouts for {current_date.strftime('%A')}")
            
            for workout in day_workouts:
                events.append({
                    'date': current_date,
                    'program_name': program.name,
                    'workout_name': workout.name
                })
            
            current_date += timedelta(days=1)
    
    print(f"\nGenerated {len(events)} total events")
    serializer = CalendarEventSerializer(events, many=True)
    print("Serialized response:", serializer.data)
    return Response(serializer.data)
