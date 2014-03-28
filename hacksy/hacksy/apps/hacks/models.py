#standard django models
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#signals
from django.db.models.signals import post_save
from django.dispatch import receiver

#django_extensions
from django_extensions.db.fields import AutoSlugField, CreationDateTimeField, ModificationDateTimeField

#project
from hackathons.models import Hackathon, HackathonMember

class Hack(models.Model):
    users = models.ManyToManyField(User,blank=True)
    name = models.CharField(max_length=100)
    hackathon = models.ForeignKey(Hackathon,blank=True,null=True)
    slug = AutoSlugField(populate_from='name',unique=True)
    code_link = models.URLField(blank=True,null=True)
    demo_link = models.URLField(blank=True,null=True)
    video_link = models.URLField(blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="hack_images",blank=True,null=True)

    views = models.IntegerField(default=0,blank=True,null=True)
    awesomeness_votes = models.ManyToManyField(User,blank=True,related_name="awesomeness_set")

    pub_date = CreationDateTimeField()
    mod_date = ModificationDateTimeField()

    def __unicode__(self):
        return self.name + ", slug:" + self.slug
    def awesomeness(self):
        return self.awesomeness_votes.count() + 1
    def get_full_name(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ("hack_detail", [self.slug])
    def prize_name(self):
        prizes = self.prize_set.all()
        if prizes:
            return prizes[0].name
        return None
    def register_view(self,commit=True):
        if not self.views:
            self.views = 0
        self.views += 1
        if commit:
            self.save()
    class Meta:
        ordering = ['-views']

admin.site.register(Hack)
