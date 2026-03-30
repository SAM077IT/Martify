from django import template

register = template.Library()

@register.filter
def underscore(value):
    """Convert spaces to underscores for URL compatibility."""
    return value.replace(" ", "_")
