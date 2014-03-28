#standard django views
from django.shortcuts import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.comments.forms import CommentForm

#python
import json

#haystack
from haystack.query import SearchQuerySet

#project
from hacks.models import Hack
from hacks.forms import HackForm

from hackathons.models import Hackathon
from endless_pagination.decorators import page_template

@page_template('hacks/hack_page.html')  # just add this decorator
def home(request, template='home.html', extra_context=None):
    context = {
        'hacks': Hack.objects.all(),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))

def ajax_hack_list_only(request):
    q = request.GET.get("q",None)
    hackathon_slug = request.GET.get("hackathon_slug",None)
    if not q:
        return HttpResponse(json.dumps({"options":[]}), content_type="application/json")
    if not hackathon_slug:
        hacks = Hack.objects.filter(name__icontains=q)
    else:
        hackathon = get_object_or_404(Hackathon,slug=hackathon_slug)
        hacks = Hack.objects.filter(name__icontains=q).filter(hackathon=hackathon)
    return HttpResponse(json.dumps({"options":[h.name for h in hacks],"pks":[h.pk for h in hacks]}), content_type="application/json")

def ajax_hack_list(request):
    q = request.GET.get("q",None)
    if not q:
        return HttpResponse(json.dumps({"options":[],"urls":[]}), content_type="application/json")
    results = SearchQuerySet().autocomplete(content_auto=q)[0:7]
    hacks = [r.object for r in results]
    data = {
        "options":[h.get_full_name()+" ["+h.__class__.__name__+"]" for h in hacks if h.get_full_name()],
        "urls":[h.get_absolute_url() for h in hacks if h.get_full_name()]
    }
    for h in hacks:
        if h.__class__.__name__ == "User" and not h.get_full_name():
            data['options'].append(h.username + " [User]")
            data['urls'].append(h.get_absolute_url())
    data["options"].append("More results")
    data["urls"].append("id_more")
    return HttpResponse(json.dumps(data), content_type="application/json")

def hack_detail(request,slug):
    hack = get_object_or_404(Hack,slug=slug)

    hack.register_view()

    context = {
        "hack": hack,
    }
    return render_to_response("hacks/hack_detail.html",context,context_instance=RequestContext(request))

def unawesome(request,slug):
    hack = get_object_or_404(Hack,slug=slug)

    result = {"awesomeness":hack.awesomeness()}
    if request.user.is_authenticated():
        if request.user in hack.awesomeness_votes.all():
            hack.awesomeness_votes.remove(request.user)
            hack.save()

    return HttpResponse(json.dumps({"awesomeness":hack.awesomeness()}), content_type="application/json")
def awesome(request,slug):
    hack = get_object_or_404(Hack,slug=slug)

    result = {"awesomeness":hack.awesomeness()}
    if request.user.is_authenticated():
        if request.user not in hack.awesomeness_votes.all():
            hack.awesomeness_votes.add(request.user)
            hack.save()

    return HttpResponse(json.dumps({"awesomeness":hack.awesomeness()}), content_type="application/json")

@login_required
def hack_create(request,slug=None):
    hack = None
    if slug:
        hack = get_object_or_404(Hack,slug=slug)
        if request.user not in hack.users.all():
            return HttpResponseRedirect(hack.get_absolute_url())
    form = HackForm(instance=hack)
    form.initial['user_list'] = [request.user]
    if request.method == "POST":
        form = HackForm(request.POST,request.FILES,instance=hack)
        form.initial = request.POST
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
        else:
            user_list = []
            for user in request.POST.getlist('users'):
                try:
                    user_list.append(User.objects.get(pk=user))
                except:
                    pass
            form.initial['user_list'] = user_list
    if hack:
        if hack.hackathon:
            form.initial['hackathon'] = hack.hackathon.name
        form.initial['user_list'] = hack.users.all()
    context = {
        "form": form
    }
    if "hackathon" in request.GET:
        form.initial['hackathon'] = get_object_or_404(Hackathon,slug=request.GET["hackathon"]).name
    if "submit" in request.GET:
        context["submit"] = True
    return render_to_response("hacks/hack_create.html",context,context_instance=RequestContext(request))

@login_required
def ajax_comment_post(request):
    print request.POST
    try:
        form = CommentForm(request.POST)
    except Exception as e:
        print e
    print "HERE"
    if form.is_valid():
        form.save()
        return HttpResponse("IT WORKED!")
    return HttpResponse("FAIL!")
