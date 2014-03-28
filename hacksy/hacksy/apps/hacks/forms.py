#standard django forms
from django import forms
from django.contrib.auth.models import User

#project
from hacks.models import Hack
from hackathons.models import HackathonMember, Hackathon
from profiles.models import Profile
from django.core.exceptions import ValidationError

from itertools import chain
import IPython
class HackForm(forms.ModelForm):
    hackathon = forms.CharField(required=False)
    def clean_users(self):
        if not self.cleaned_data['users']:
            raise ValidationError("Must provide at least one hacker")
        return self.cleaned_data['users']
    def clean_hackathon(self):
        h = self.cleaned_data['hackathon']
        if h:
            try:
                h = Hackathon.objects.get(name=h)
            except Hackathon.DoesNotExist:
                raise ValidationError("Please enter a valid hackathon name")
            self.cleaned_data['hackathons'] = h
            return h
        return None
    def save(self):
        instance = super(HackForm,self).save()
        instance.hackathon = self.cleaned_data['hackathon']
        instance.save()
        return instance
    def __init__(self, *args, **kwargs):
        super(HackForm, self).__init__(*args, **kwargs)
        self.fields['users'].error_messages['invalid_pk_value']._proxy____args = (u'%s - All hackers must be registered on Hacksy. Have your other team members sign up. It only takes a few seconds ;)',)
    class Meta:
        model = Hack
        exclude = ("slug","hackathon","awesomeness","views")
