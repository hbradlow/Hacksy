#standard django
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

#python
import urllib2

#django_extensions
from django_extensions.db.fields import CreationDateTimeField

#social auth
from social_auth.models import UserSocialAuth

#signals
from django.db.models.signals import post_save
from django.dispatch import receiver

#github
from github import Github

#project
from hacks.models import Hack

class Profile(models.Model):
    user = models.OneToOneField(User)
    first_language = models.CharField(max_length=100,null=True,blank=True)
    location = models.CharField(max_length=100,null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="profile_images",null=True,blank=True)
    joined = CreationDateTimeField()
    def __unicode__(self):
        return "User: " + str(self.user)
    def hindex(self):
        hacks = self.user.hack_set.all()
        counter = {}
        for hack in hacks:
            a = hack.awesomeness_votes.count()
            if a in counter:
                counter[a] += 1
            else:
                counter[a] = 1
        max = 0
        for key,value in counter.items():
            if value >= key and key > max:
                max = key
        return max + 1
    def reputation(self):
        return self.hindex()
    def get_absolute_url(self):
        return self.user.get_absolute_url()
    def hacks(self):
        return self.user.hack_set.all()
    def hackathons(self):
        hacks = self.user.hack_set.all()
        hs = set()
        for hack in hacks:
            hs.add(hack.hackathon)
        return hs
    def team_for_hackathon(self,hackathon):
        team = None
        members = self.user.hackathonmember_set.all()
        for member in members:
            for t in member.team_set.all():
                if t in hackathon.teams.all():
                    team = t
        return team

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    """
        Creates a Profile model for each User that is created.

        This function is called on the post_save signal from User.
    """
    u = instance

    if created:
        p = Profile.objects.create(user=u)
        if not u.last_name:
            names = u.first_name.split(" ")
            if len(names)>1:
                u.last_name = names[1]
                u.save()

    if not u.get_profile().image:
        # get gravatar
        user_sa = UserSocialAuth.objects.filter(user=u)
        if user_sa:
            user_sa = user_sa[0]
            token = user_sa.extra_data['access_token'] 
            g = Github(token).get_user()
            gravatar_id = g.gravatar_id
            url = "https://secure.gravatar.com/avatar/" + gravatar_id + "?s=500"

            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urllib2.urlopen(url).read())
            img_temp.flush()
            u.get_profile().image.save("gravatar_image_" + str(u.pk), File(img_temp))

admin.site.register(Profile)
