from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import base64
import openai
from PIL import Image
import io

class FoodImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='food_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def analyze_image(self):
        """Use OpenAI's Vision model to analyze the food in the image"""
        if not self.image:
            return None
            
        try:
            # Verify API key
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                print("Error: OpenAI API key is not configured")
                return None
            if not api_key.startswith('sk-'):
                print("Error: Invalid OpenAI API key format")
                return None
            print("API key validation successful")

            # Process and encode the image
            print("Processing image...")
            try:
                # Open and resize image if needed
                with Image.open(self.image) as img:
                    # Convert to RGB if image is in RGBA mode
                    if img.mode == 'RGBA':
                        img = img.convert('RGB')
                    
                    # Calculate current size in MB
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG', quality=95)
                    current_size = len(img_byte_arr.getvalue()) / (1024 * 1024)  # Size in MB
                    
                    # Resize if larger than 20MB
                    while current_size > 20:
                        # Calculate new dimensions (reduce by 10% each iteration)
                        width, height = img.size
                        new_width = int(width * 0.9)
                        new_height = int(height * 0.9)
                        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Check new size
                        img_byte_arr = io.BytesIO()
                        img.save(img_byte_arr, format='JPEG', quality=95)
                        current_size = len(img_byte_arr.getvalue()) / (1024 * 1024)
                    
                    # Get final image data
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG', quality=95)
                    image_data = img_byte_arr.getvalue()
                    base64_image = base64.b64encode(image_data).decode('utf-8')
                    print(f"Image processed and encoded (Size: {current_size:.2f}MB)")
            except Exception as e:
                print(f"Error processing image: {str(e)}")
                return None

            # Create the API request
            print("Sending request to OpenAI API...")
            try:
                # Create OpenAI client
                client = openai.OpenAI(api_key=api_key)
                
                # Create API request
                print("Making API request with image size:", len(base64_image))
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this food image and return a JSON array of food items. Each item should have 'name', 'quantity', and 'unit' fields. For quantities, use numerical values and appropriate units from this list: grams (g), milliliters (ml), ounces (oz), cups (cup), tablespoons (tbsp), teaspoons (tsp), or pieces (piece). Here are examples of how to format different types of foods:\n\n[{\n  \"name\": \"Grilled Chicken Breast\",\n  \"quantity\": 100,\n  \"unit\": \"g\"\n},\n{\n  \"name\": \"Mixed Salad Greens\",\n  \"quantity\": 2,\n  \"unit\": \"cup\"\n},\n{\n  \"name\": \"Olive Oil Dressing\",\n  \"quantity\": 2,\n  \"unit\": \"tbsp\"\n},\n{\n  \"name\": \"Cherry Tomatoes\",\n  \"quantity\": 6,\n  \"unit\": \"piece\"\n},\n{\n  \"name\": \"Avocado\",\n  \"quantity\": 0.5,\n  \"unit\": \"piece\"\n}]\n\nPlease format your response exactly like this example, using appropriate units for each food item."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }],
                    max_tokens=300
                )
                print("Response received:", response)

                # Validate response
                if not hasattr(response, 'choices') or not response.choices:
                    print("Error: Invalid response format from OpenAI API")
                    return None
                print("API request successful")
            except openai.APIError as e:
                print(f"OpenAI API Error: {str(e)}")
                return None
            except Exception as e:
                print(f"Unexpected error during API call: {str(e)}")
                return None
            print("Received response from OpenAI API")
            
            self.processed = True
            self.save()
            
            # Get and process the content from the response
            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                
                # Remove markdown code block if present
                if content.startswith('```') and content.endswith('```'):
                    # Extract content between first and last ```
                    content = content.split('```')[1]
                    # Remove json language identifier if present
                    if content.startswith('json\n'):
                        content = content[5:]
                    elif content.startswith('json'):
                        content = content[4:]
                    content = content.strip()
                
                return content
            return None
        except Exception as e:
            import traceback
            print(f"Error analyzing image: {str(e)}")
            print("Full error details:")
            print(traceback.format_exc())
            return None

class FoodItem(models.Model):
    UNIT_CHOICES = [
        ('g', 'grams'),
        ('ml', 'milliliters'),
        ('oz', 'ounces'),
        ('cup', 'cups'),
        ('tbsp', 'tablespoons'),
        ('tsp', 'teaspoons'),
        ('piece', 'pieces'),
    ]

    meal = models.ForeignKey('Meal', on_delete=models.CASCADE, related_name='food_items')
    name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    calories = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    protein = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    carbs = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    fat = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.name}"

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_image = models.ForeignKey(FoodImage, on_delete=models.SET_NULL, null=True, blank=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.get_meal_type_display()} on {self.date}"

    @property
    def total_calories(self):
        return sum(item.calories for item in self.food_items.all())

    @property
    def total_protein(self):
        return sum(item.protein for item in self.food_items.all())

    @property
    def total_carbs(self):
        return sum(item.carbs for item in self.food_items.all())

    @property
    def total_fat(self):
        return sum(item.fat for item in self.food_items.all())
