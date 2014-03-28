#standard django
from django.shortcuts import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

#python
import json

#project
from profiles.forms import ProfileForm, UserForm

@login_required
def profile(request):
    u = request.user
    return HttpResponseRedirect(reverse("user_profile",args=(u.username,)))

def user_create(request):
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request,user)
            return HttpResponseRedirect(user.get_absolute_url())
    return render_to_response("profiles/user_create.html",{"form":form},context_instance=RequestContext(request))

def ajax_profile_list(request):
    q = request.GET.get("q",None)
    if not q:
        return HttpResponse(json.dumps({"options":[]}), content_type="application/json")
    users = User.objects.filter(username__icontains=q)
    images = []
    for u in users:
        if u.get_profile().image:
            images.append(u.get_profile().image.url)
        else:
            images.append(None)
    data = {
        "options":[u.username for u in users],
        "pks":[u.pk for u in users],
        "images":images
    }
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required
def profile_edit(request,username=None):
    profile = request.user.get_profile()
    form = ProfileForm(instance=profile)
    form.initial['username'] = profile.user.username
    if request.method=="POST":
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        form.initial['username'] = profile.user.username
        form.initial = request.POST
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    return render_to_response("profiles/profile_create.html",{"form":form},context_instance=RequestContext(request))

def user_profile(request,username):
    print username
    u = get_object_or_404(User,username=username)
    context = {
        "profile":u.get_profile(),
    }
    return render_to_response("profiles/profile.html",context,context_instance=RequestContext(request))
