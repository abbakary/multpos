from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def custom_date(value):
    """Format date as 'Sep 22, 2025 10:38'"""
    if not value:
        return ''
    
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    
    # Convert to local timezone if needed
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    
    return value.strftime('%b %d, %Y %H:%M')

@register.filter
def custom_date_only(value):
    """Format date as 'Sep 22, 2025'"""
    if not value:
        return ''
    
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except:
            return value
    
    # Convert to local timezone if needed
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    
    return value.strftime('%b %d, %Y')