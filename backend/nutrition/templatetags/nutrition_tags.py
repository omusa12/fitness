from django import template

register = template.Library()

@register.simple_tag
def macro_percentage(value, total_calories):
    """Calculate the percentage of calories from a macro nutrient and return formatted style"""
    if not total_calories or not value:
        return "width: 0%"
    
    try:
        percentage = (float(value) / float(total_calories)) * 100
        percentage = min(percentage, 100)  # Cap at 100%
        return f"width: {percentage:.0f}%"
    except (ValueError, ZeroDivisionError):
        return "width: 0%"
