from django import template
from django.template.loader import get_template
register = template.Library()
t = get_template('joan/feature_status.html')

@register.inclusion_tag(t)
def show_feature_status(feature):
    return {'feature': feature}
