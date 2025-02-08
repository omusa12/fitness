import json
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Prefetch
from .models import Meal, FoodItem, FoodImage
from .serializers import MealSerializer, FoodItemSerializer, FoodImageSerializer

class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)\
            .prefetch_related(
                Prefetch('food_items', queryset=FoodItem.objects.all())
            )\
            .order_by('-date', '-time')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def analyze_image(self, request):
        """Upload and analyze a food image"""
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the food image
        food_image = FoodImage(user=request.user, image=request.FILES['image'])
        food_image.save()

        # Analyze the image
        analysis_result = food_image.analyze_image()
        if not analysis_result:
            food_image.delete()
            return Response(
                {'error': 'Failed to analyze image'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Parse the analysis result
            detected_items = json.loads(analysis_result)
            return Response({
                'food_image_id': food_image.id,
                'detected_items': detected_items
            })
        except json.JSONDecodeError:
            food_image.delete()
            return Response(
                {'error': 'Invalid analysis result'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def add_food_item(self, request, pk=None):
        meal = self.get_object()
        serializer = FoodItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(meal=meal)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
