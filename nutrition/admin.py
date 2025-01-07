from django.contrib import admin
from .models import FoodImage, FoodItem, Meal

@admin.register(FoodImage)
class FoodImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at', 'processed')
    list_filter = ('processed', 'uploaded_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('uploaded_at',)

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'meal', 'quantity', 'unit', 'calories', 'protein', 'carbs', 'fat', 'verified')
    list_filter = ('verified', 'unit')
    search_fields = ('name', 'meal__user__username')
    list_editable = ('verified',)

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('user', 'meal_type', 'date', 'time', 'total_calories', 'total_protein', 'total_carbs', 'total_fat')
    list_filter = ('meal_type', 'date')
    search_fields = ('user__username', 'notes')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'

    def get_queryset(self, request):
        """Prefetch related food items to avoid N+1 queries when calculating totals"""
        return super().get_queryset(request).prefetch_related('food_items')
