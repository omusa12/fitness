from rest_framework import serializers
from .models import Meal, FoodItem, FoodImage

class FoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodImage
        fields = ['id', 'image', 'uploaded_at', 'processed']

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'quantity', 'unit', 'calories', 'protein', 'carbs', 'fat', 'verified']

class MealSerializer(serializers.ModelSerializer):
    food_items = FoodItemSerializer(many=True, read_only=True)
    meal_type_display = serializers.CharField(source='get_meal_type_display', read_only=True)
    total_calories = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    total_protein = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    total_carbs = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)
    total_fat = serializers.DecimalField(max_digits=7, decimal_places=2, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'meal_type', 'meal_type_display', 'date', 'time', 'notes', 
                 'food_items', 'food_image', 'total_calories', 'total_protein', 'total_carbs', 'total_fat']
