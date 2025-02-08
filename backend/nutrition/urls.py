from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

app_name = 'nutrition'

router = DefaultRouter()
router.register(r'api/meals', api.MealViewSet, basename='meal-api')

urlpatterns = [
    path('', include(router.urls)),
    path('upload/', views.upload_food_image, name='upload_food_image'),
    path('create-meal/', views.create_meal, name='create_meal'),
    path('meals/', views.meal_list, name='meal_list'),
    path('meal/<int:meal_id>/', views.meal_detail, name='meal_detail'),
    path('meal/<int:meal_id>/edit-items/', views.edit_food_items, name='edit_food_items'),
    path('food-item/<int:item_id>/verify/', views.verify_food_item, name='verify_food_item'),
]
