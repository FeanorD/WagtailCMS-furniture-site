
from django import template

from wagtail.core.models import Page

from home.models import FooterText

register = template.Library()

@register.inclusion_tag('home/include/footer_contacts.html', takes_context=True)
def get_footer_text(context):
    return {
        'footer_contacts': FooterText.objects.all(),
        'request': context['request'],
    }


@register.inclusion_tag('home/include/contact_us.html', takes_context=True)
def get_contacts(context):
    return {
        'footer_contacts': FooterText.objects.all(),
        'request': context['request'],      
    }