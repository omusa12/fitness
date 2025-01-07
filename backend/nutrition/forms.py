from django import forms
from .models import FoodImage, Meal, FoodItem

class FoodImageUploadForm(forms.ModelForm):
    class Meta:
        model = FoodImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
        }

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_type', 'date', 'time', 'notes']
        widgets = {
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'quantity', 'unit', 'calories', 'protein', 'carbs', 'fat']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class FoodItemFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = FoodItem.objects.none()

def get_food_item_formset(extra=1):
    return forms.modelformset_factory(
        FoodItem,
        form=FoodItemForm,
        formset=FoodItemFormSet,
        extra=extra,
        can_delete=True
    )

# Default formset with one extra form
FoodItemFormSetFactory = get_food_item_formset(extra=1)
