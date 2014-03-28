#standard django models
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#signals
from django.db.models.signals import post_save
from django.dispatch import receiver

#django_extensions
from django_extensions.db.fields import AutoSlugField, CreationDateTimeField, ModificationDateTimeField

class BlogPost(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="name",unique=True)
    author = models.ForeignKey(User,limit_choices_to={"is_staff": True})
    pub_date = CreationDateTimeField()
    content = models.TextField()
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ("blogpost_detail", [self.slug])
admin.site.register(BlogPost)
