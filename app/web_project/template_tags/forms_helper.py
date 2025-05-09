from django import template
from django.utils.safestring import SafeString

register = template.Library()
@register.filter(name='add_class')
def add_class(field, css_class):
    """Adds a CSS class to a form field."""
    return field.as_widget(attrs={'class': css_class})

# attr
@register.filter(name='attr')
def attr(field, attributes):
    """Adds an attribute to a form field."""
    attr_name, attr_value = attributes.split(':')
    
    # Check if the field is already a SafeString (rendered)
    if isinstance(field, SafeString):
        # In this case, we can't modify it anymore as it's already rendered
        return field
    
    # If it's a BoundField, we can add attributes
    return field.as_widget(attrs={attr_name: attr_value})
