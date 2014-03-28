#standard django views
from django.shortcuts import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.sites.models import Site

#standard python
import json
import datetime

#project
from hackathons.models import Hackathon, Team
from hackathons.forms import HackathonForm, TeamForm, JudgeForm, PrizeForm, SponsorForm

#eventbrite
import eventbrite

#csv
import csv

def hackathon_csv(request,slug):
    hackathon = get_object_or_404(Hackathon,slug=slug)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + hackathon.slug + '"'

    writer = csv.writer(response)
    writer.writerow(["Hack name", "url", "description", "users"])
    for hack in hackathon.hack_set.all():
        user_string = ",".join([u.username for u in hack.users.all()])
        writer.writerow([hack.name, str(Site.objects.all()[0].domain) + hack.get_absolute_url(), hack.description, user_string])
    return response

def hackathon_list(request):
    hackathons = Hackathon.objects.all()
    context = {
        "hackathons": hackathons,
    }
    return render_to_response("hackathons/hackathon_list.html",context,context_instance=RequestContext(request))

def prize_edit(request,hackathon_slug):
    hackathon = get_object_or_404(Hackathon,slug=hackathon_slug)
    form = PrizeForm()
    if request.method == "POST":
        form = PrizeForm(request.POST,request.FILES)
        form.initial = request.POST
        if form.is_valid():
            form.save()
            hackathon.prizes.add(form.instance)
            hackathon.save()
            return HttpResponseRedirect(hackathon.get_absolute_url())
    context = {
        "form": form,
        "hackathon": hackathon
    }
    return render_to_response("hackathons/prize_edit.html",context,context_instance=RequestContext(request))
def sponsor_edit(request,hackathon_slug):
    hackathon = get_object_or_404(Hackathon,slug=hackathon_slug)
    form = SponsorForm()
    if request.method == "POST":
        form = SponsorForm(request.POST,request.FILES)
        form.initial = request.POST
        if form.is_valid():
            form.save()
            hackathon.sponsors.add(form.instance)
            hackathon.save()
            return HttpResponseRedirect(hackathon.get_absolute_url())
    context = {
        "form": form,
        "hackathon": hackathon
    }
    return render_to_response("hackathons/sponsor_edit.html",context,context_instance=RequestContext(request))
def judge_edit(request,hackathon_slug):
    hackathon = get_object_or_404(Hackathon,slug=hackathon_slug)
    form = JudgeForm()
    if request.method == "POST":
        form = JudgeForm(request.POST,request.FILES)
        form.initial = request.POST
        if form.is_valid():
            form.save()
            hackathon.judges.add(form.instance)
            hackathon.save()
            return HttpResponseRedirect(hackathon.get_absolute_url())
    context = {
        "form": form,
        "hackathon": hackathon
    }
    return render_to_response("hackathons/judge_edit.html",context,context_instance=RequestContext(request))

def ajax_hackathon_list(request):
    q = request.GET.get("q",None)
    if not q:
        return HttpResponse(json.dumps({"options":[]}), content_type="application/json")
    hackathons = Hackathon.objects.filter(name__icontains=q)
    return HttpResponse(json.dumps({"options":[h.name for h in hackathons],"pks":[h.pk for h in hackathons]}), content_type="application/json")

def hackathon_detail(request,slug):
    hackathon = get_object_or_404(Hackathon,slug=slug)
    hackathon.register_view()
    form = HackathonForm()
    context = {
        "hackathon": hackathon,
        "form": form,
    }
    return render_to_response("hackathons/hackathon_detail.html",context,context_instance=RequestContext(request))

@login_required
def dashboard(request,slug):
    hackathon = get_object_or_404(Hackathon,slug=slug)
    #the user must be part of a team for this hacakthon to view the dashboard

    """
    team = request.user.get_profile().team_for_hackathon(hackathon)
    if not team:
        return HttpResponseRedirect(reverse("team_create") + "?hackathon=" + hackathon.slug)
    """

    context = {
        "hackathon": hackathon,
    }
    return render_to_response("hackathons/dashboard.html",context,context_instance=RequestContext(request))

def team_detail(request,slug):
    team = get_object_or_404(Team,slug=slug)
    form = TeamForm()
    context = {
        "team": team,
        "form": form,
    }
    return render_to_response("hackathons/team_detail.html",context,context_instance=RequestContext(request))

@login_required
def hackathon_create(request,slug=None):
    instance = None
    if slug:
        instance = get_object_or_404(Hackathon,slug=slug)
    form = HackathonForm(instance=instance)
    if request.method == "POST":
        form = HackathonForm(request.POST,request.FILES,instance=instance)
        form.initial = request.POST
        if form.is_valid():
            form.save()
            hackathon = form.instance
            hackathon.admin.add(request.user) #add the current user to the admin
            hackathon.save()

            return HttpResponseRedirect(form.instance.get_absolute_url())
    context = {
        "form": form
    }
    if instance:
        context['hackathon'] = instance
    return render_to_response("hackathons/hackathon_create.html",context,context_instance=RequestContext(request))

@login_required
def ajax_hackathon_edit(request,slug):
    hackathon = get_object_or_404(Hackathon,slug=slug)
    if request.method == "POST":
        form = HackathonForm(request.POST,request.FILES,instance=hackathon)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({"success":True}))
    return HttpResponse(json.dumps({"success":False}))

@login_required
def team_create(request,slug=None):
    hackathon = None
    if "hackathon" in request.GET:
        hackathon = get_object_or_404(Hackathon,slug=request.GET["hackathon"])

    instance = None
    if slug:
        instance = get_object_or_404(Team,slug=slug)
    form = TeamForm(instance=instance)
    if request.method == "POST":
        form = TeamForm(request.POST,request.FILES,instance=instance)
        form.hackathon = hackathon
        if form.is_valid():
            form.save()
            team = form.instance
            hackathon.teams.add(team)
            hackathon.save()
            return HttpResponseRedirect(reverse("dashboard",args=(hackathon.slug,)))
    return render_to_response("hackathons/team_create.html",{"form":form},context_instance=RequestContext(request))
