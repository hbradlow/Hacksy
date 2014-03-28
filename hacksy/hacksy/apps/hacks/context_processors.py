from hacks.models import Hack
from django.contrib.sites.models import Site
def hacks(request):
    return {"hacks":Hack.objects.all()}
def site(request):
    return {"site":Site.objects.all()[0]}
