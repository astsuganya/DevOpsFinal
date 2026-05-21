import os
from django import template

register = template.Library()

@register.filter
def file_exists(image_field):
    """
    Returns True if the image field has a value AND is accessible.
    - Cloudinary URL (starts with http) → True เสมอ
    - Local file → ตรวจว่ามีอยู่จริงบน disk
    """
    if not image_field:
        return False
    try:
        url = image_field.url
        # Cloudinary or any external URL — assume it exists
        if url.startswith('http'):
            return True
        # Local file — check disk
        return os.path.exists(image_field.path)
    except Exception:
        return False
