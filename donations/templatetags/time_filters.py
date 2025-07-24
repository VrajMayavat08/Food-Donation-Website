from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def format_duration(seconds):
    """
    Convert seconds into a human-readable format: days, hours, minutes
    """
    if seconds is None or seconds == "Not available":
        return "Not available"
    
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "Invalid value"
    
    if seconds < 0:
        return "Invalid value"
    
    # Calculate days, hours, minutes
    days = seconds // 86400  # 86400 seconds in a day
    hours = (seconds % 86400) // 3600  # 3600 seconds in an hour
    minutes = (seconds % 3600) // 60  # 60 seconds in a minute
    remaining_seconds = seconds % 60
    
    # Build the formatted string
    parts = []
    
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    
    # Only show seconds if less than a minute
    if seconds < 60:
        parts.append(f"{remaining_seconds} second{'s' if remaining_seconds != 1 else ''}")
    
    if not parts:
        return "0 seconds"
    
    return ", ".join(parts)

@register.filter
def format_duration_short(seconds):
    """
    Convert seconds into a short format: d h m
    """
    if seconds is None or seconds == "Not available":
        return "N/A"
    
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "N/A"
    
    if seconds < 0:
        return "N/A"
    
    # Calculate days, hours, minutes
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    
    # Build the short formatted string
    parts = []
    
    if days > 0:
        parts.append(f"{days}d")
    
    if hours > 0:
        parts.append(f"{hours}h")
    
    if minutes > 0:
        parts.append(f"{minutes}m")
    
    # Show seconds if less than a minute
    if seconds < 60:
        parts.append(f"{remaining_seconds}s")
    
    if not parts:
        return "0s"
    
    return " ".join(parts) 