import os
from django import template

register = template.Library()

@register.filter
def file_exists(image_field):
    """Returns True if the image field has a value AND the file exists on disk."""
    if not image_field:
        return False
    try:
        return os.path.exists(image_field.path)
    except Exception:
        return False
