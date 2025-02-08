import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ValidationError
from .models import FoodImage, Meal, FoodItem
from .forms import FoodImageUploadForm, MealForm, FoodItemForm, get_food_item_formset

@login_required
def upload_food_image(request):
    if request.method == 'POST':
        form = FoodImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            food_image = form.save(commit=False)
            food_image.user = request.user
            food_image.save()
            
            # Analyze the image using OpenAI Vision
            analysis_result = food_image.analyze_image()
            
            if analysis_result:
                try:
                    # Parse the JSON response from OpenAI
                    detected_items = json.loads(analysis_result)
                    
                    # Store the detected items in session for the next step
                    request.session['detected_items'] = detected_items
                    request.session['food_image_id'] = food_image.id
                    
                    return redirect('nutrition:create_meal')
                except json.JSONDecodeError:
                    messages.error(request, "Error processing the image analysis results.")
            else:
                messages.error(request, "Could not analyze the image. Please try again.")
            
            return redirect('nutrition:upload_food_image')
    else:
        form = FoodImageUploadForm()
    
    return render(request, 'nutrition/upload_food_image.html', {'form': form})

@login_required
def create_meal(request):
    detected_items = request.session.get('detected_items', [])
    food_image_id = request.session.get('food_image_id')
    
    if not detected_items or not food_image_id:
        messages.error(request, "No food items detected. Please upload an image first.")
        return redirect('nutrition:upload_food_image')
    
    if request.method == 'POST':
        meal_form = MealForm(request.POST)
        # Get the number of items from the session
        initial_data = request.session.get('detected_items', [])
        if not isinstance(initial_data, list):
            initial_data = []
        num_items = len(initial_data)
        FormSetFactory = get_food_item_formset(extra=num_items + 1)
        formset = FormSetFactory(request.POST)
        
        if meal_form.is_valid() and formset.is_valid():
            meal = meal_form.save(commit=False)
            meal.user = request.user
            meal.food_image_id = food_image_id
            meal.save()
            
            # Save food items
            instances = formset.save(commit=False)
            for instance in instances:
                instance.meal = meal
                instance.save()
            
            # Clean up session
            del request.session['detected_items']
            del request.session['food_image_id']
            
            messages.success(request, "Meal created successfully!")
            return redirect('nutrition:meal_detail', meal_id=meal.id)
    else:
        meal_form = MealForm()
        # Process detected items to ensure correct field mapping
        initial_data = []
        if isinstance(detected_items, list):
            for item in detected_items:
                if isinstance(item, dict):
                    # Ensure all required fields are present with correct names
                    processed_item = {
                        'name': item.get('name', ''),
                        'quantity': item.get('quantity', 0),
                        'unit': item.get('unit', ''),  # This must match exactly with UNIT_CHOICES
                        'calories': item.get('calories', 0),
                        'protein': item.get('protein', 0),
                        'carbs': item.get('calories', 0),  # Map calories to carbs since they're the same
                        'fat': item.get('fat', 0)
                    }
                    initial_data.append(processed_item)
        
        # Set the number of forms to match the detected items plus one extra
        num_items = len(initial_data)
        FormSetFactory = get_food_item_formset(extra=num_items + 1)
        formset = FormSetFactory(initial=initial_data)
    
    return render(request, 'nutrition/create_meal.html', {
        'meal_form': meal_form,
        'formset': formset,
    })

@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'nutrition/meal_list.html', {'meals': meals})

@login_required
def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, "Meal updated successfully!")
            return redirect('nutrition:meal_detail', meal_id=meal.id)
    else:
        form = MealForm(instance=meal)
    
    return render(request, 'nutrition/meal_detail.html', {
        'meal': meal,
        'form': form,
    })

@login_required
def edit_food_items(request, meal_id):
    meal = get_object_or_404(Meal, id=meal_id, user=request.user)
    
    if request.method == 'POST':
        FormSetFactory = get_food_item_formset(extra=1)
        formset = FormSetFactory(request.POST, queryset=meal.food_items.all())
        if formset.is_valid():
            instances = formset.save(commit=False)
            
            # Handle deleted instances
            for obj in formset.deleted_objects:
                obj.delete()
            
            # Save new/updated instances
            for instance in instances:
                instance.meal = meal
                instance.save()
            
            messages.success(request, "Food items updated successfully!")
            return redirect('nutrition:meal_detail', meal_id=meal.id)
    else:
        FormSetFactory = get_food_item_formset(extra=1)
        formset = FormSetFactory(queryset=meal.food_items.all())
    
    return render(request, 'nutrition/edit_food_items.html', {
        'meal': meal,
        'formset': formset,
    })

@login_required
@require_POST
def verify_food_item(request, item_id):
    food_item = get_object_or_404(FoodItem, id=item_id, meal__user=request.user)
    food_item.verified = True
    food_item.save()
    return JsonResponse({'status': 'success'})
