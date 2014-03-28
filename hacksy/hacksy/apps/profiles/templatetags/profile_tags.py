from django import template
from hacks.models import Hack

register = template.Library()

@register.filter
def hack_for_hackathon_name(user,hackathon):
    hacks = Hack.objects.filter(hackathon=hackathon).filter(users__in=[user.pk])
    if hacks:
        return hacks[0].name
    return None
@register.filter
def hack_for_hackathon_url(user,hackathon):
    hacks = Hack.objects.filter(hackathon=hackathon).filter(users__in=[user.pk])
    if hacks:
        return hacks[0].get_absolute_url()
    return None

@register.filter
def klass(value):
    return value.__class__.__name__
