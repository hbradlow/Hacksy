from django import forms
from profiles.models import Profile
from django.contrib.auth.models import User

from hackathons.models import Hackathon, Team, HackathonMember, Event, Judge, Sponsor, Prize
from hacks.models import Hack

from django.core.exceptions import ValidationError

import datetime

from dateutil import parser
from dateutil import tz 

import IPython

class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
class PrizeForm(forms.ModelForm):
    hack = forms.CharField(required=True)
    def clean_hack(self):
        h = self.cleaned_data['hack']
        h = Hack.objects.filter(name=h)
        if not h:
            return None
        return h[0]
    def save(self):
        instance = super(PrizeForm,self).save()
        instance.hack = self.cleaned_data['hack']
        instance.save()
        return instance
    class Meta:
        model = Prize
class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor

class HackathonForm(forms.ModelForm):
    start_time = forms.SplitDateTimeField(input_time_formats=['%I:%M %p'])
    end_time = forms.SplitDateTimeField(input_time_formats=['%I:%M %p'])
    events = forms.CharField(required=False)
    def clean_events(self):
        e = self.cleaned_data["events"]
        es = []
        for event in e.split("-----"):
            l = event.split(":::::")
            if len(l) == 2:
                name,t = l
                cet = tz.gettz('UTC')
                t = parser.parse(t)
                t.replace(tzinfo = cet)
                e = Event(name=name,time=t)
                es.append(e)
        return es
    def save(self,commit=True):
        instance = super(HackathonForm,self).save(commit=commit)
        for e in instance.event_set.all():
            e.delete()
        for e in self.cleaned_data['events']:
            e.hackathon = instance
            e.save()
        instance.save()
        return instance
    class Meta:
        model = Hackathon
        exclude = ("admin","judges","teams","winners",)

class TeamForm(forms.ModelForm):
    hackers = forms.CharField()
    def clean_hackers(self):
        data = self.cleaned_data['hackers']
        hackers = []
        for hacker in data.split(","):
            hacker = hacker.strip()
            users = User.objects.filter(username=hacker)
            if users:
                if self.hackathon:
                    if users[0].get_profile().team_for_hackathon(self.hackathon):
                        raise ValidationError(str(users[0]) + u' is already on a team for this hackathon')
                h = HackathonMember.objects.create(user=users[0])
                hackers.append(h)
            else:
                h = HackathonMember.objects.create(name=hacker)
                hackers.append(h)
        return hackers
    def save(self,commit=True):
        instance = super(TeamForm,self).save(commit=commit)

        instance.users = self.cleaned_data['hackers']
        instance.save()

        return instance
    class Meta:
        model = Team
        exclude = ("users","slug",)
