#standard django models
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

#signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

#django_extensions
from django_extensions.db.fields import AutoSlugField

#timezone
from django.utils import timezone
from django.utils.timezone import get_default_timezone

class HackathonMember(models.Model):
    """
        Intermediate model so that anonymous users can be added as hackers.
    """
    user = models.ForeignKey(User,null=True,blank=True)
    name = models.CharField(max_length=100,blank=True,null=True)
@receiver(pre_save,sender=HackathonMember)
def create_hackathon_name(sender,instance,**kwargs):
    """
        Creates a Profile model for each User that is created.

        This function is called on the post_save signal from User.
    """
    if instance.user:
        instance.name = instance.user.get_full_name()
admin.site.register(HackathonMember)

class Team(models.Model):
    users = models.ManyToManyField(HackathonMember,blank=True)
    description = models.TextField(blank=True,null=True)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name',unique=True)
    def __unicode__(self):
        return self.name
    @models.permalink
    def get_absolute_url(self):
        return ("team_detail", [self.slug])
admin.site.register(Team)

class Prize(models.Model):
    hack = models.ForeignKey("hacks.Hack",null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    rank = models.IntegerField()
    class Meta:
        ordering = ["-rank"]
admin.site.register(Prize)

class Sponsor(models.Model):
    image = models.ImageField(upload_to="judge_images",null=True,blank=True)
    name = models.CharField(max_length=500)
admin.site.register(Sponsor)

class Judge(models.Model):
    image = models.ImageField(upload_to="judge_images",null=True,blank=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
admin.site.register(Judge)

class Hackathon(models.Model):
    admin = models.ManyToManyField(User,blank=True,related_name="admin_set")
    judges = models.ManyToManyField(Judge,blank=True,related_name="judge_set")
    sponsors = models.ManyToManyField(Sponsor,blank=True,related_name="judge_set")
    teams = models.ManyToManyField(Team,blank=True,related_name="team_set")
    prizes = models.ManyToManyField(Prize,blank=True)

    eventbrite_url = models.URLField(null=True,blank=True)

    name = models.CharField(max_length=100,unique=True)
    slug = AutoSlugField(populate_from='name',unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="hackathon_images",blank=True,null=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=500)
    location_notes= models.TextField(null=True,blank=True)

    views = models.IntegerField(default=0,blank=True,null=True)

    def __unicode__(self):
        return self.name + ", slug:" + self.slug
    @models.permalink
    def get_absolute_url(self):
        return ("hackathon_detail", [self.slug])
    def get_full_name(self):
        return self.name
    def total_duration(self):
        return self.end_time-self.start_time
    def register_view(self,commit=True):
        if not self.views:
            self.views = 0
        self.views += 1
        if commit:
            self.save()
    def events_string(self):
        t = lambda e: e.time.replace(tzinfo=get_default_timezone())
        return "-----".join([e.name + ":::::" + t(e).date().strftime("%m/%d/%Y") + " " + t(e).time().strftime("%I:%M %p") for e in self.event_set.all()])
    def google_date_range(self):
        """
            Render the time duration of this hackathon as a string that can be passed to the google calandar api.
        """
        def convert_datetime(dt):
            d = dt.date()
            d_s = d.strftime("%Y%m%d")
            t = dt.time()
            t_s = t.strftime("%H%M%S")
            return d_s + "T" + t_s + "Z" 
        return convert_datetime(self.start_time) + "/" + convert_datetime(self.end_time)
    def time_before_demo(self):
        """
            Returns the time before the end of the hackathon.

            If the hackathon is already over, return 0.
            If the hackathon has not yet begun, return -1.
        """
        dif = self.end_time - timezone.now() #time before the end
        sdif = self.end_time - self.start_time #duration of the event
        if dif.total_seconds() < 0: #end_time is before now
            return 0
        elif dif.total_seconds() > sdif.total_seconds():
            return -1
        return dif
    def percent_complete(self):
        """
            Percentage of the event that has been completed.

            Bounded by 0 and 100.
        """
        if self.end_time == self.start_time:
            #degenerate case: if end_time==start_time, return 100
            return 100
        return max(0,min(100,100*((timezone.now()-self.start_time).total_seconds())/((self.end_time-self.start_time).total_seconds())))
    def next_event(self):
        """
            Return the next event that will occur.

            This is the least event greater than the current time.
        """
        now = timezone.now()
        events = self.event_set.filter(time__gte=now)
        if events:
            return events[0]
        return None
admin.site.register(Hackathon)

class Event(models.Model):
    time = models.DateTimeField()
    name = models.CharField(max_length=100)
    hackathon = models.ForeignKey(Hackathon)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['time']
admin.site.register(Event)
