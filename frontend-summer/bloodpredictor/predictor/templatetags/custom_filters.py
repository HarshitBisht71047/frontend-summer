from django import template

register = template.Library()

@register.filter
def underscore_to_space(value):
    """Replaces underscores with spaces and converts to title case."""
    return value.replace('_', ' ').title()
