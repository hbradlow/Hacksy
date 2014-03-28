#standard django forms
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

#project
from profiles.models import Profile

class UserForm(forms.ModelForm):
    password_again = forms.CharField()
    def clean_email(self):
        if not self.cleaned_data['email']:
            raise ValidationError("Please enter an email address.")
        return self.cleaned_data['email']
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            u = User.objects.get(username=username)
            raise ValidationError("That username is taken.")
        except User.DoesNotExist:
            return username
    def clean_password_again(self):
        p = self.cleaned_data['password']
        p_a = self.cleaned_data['password_again']
        if p != p_a:
            raise ValidationError("Passwords do not match.")
        return p_a
    def save(self,commit=True):
        return User.objects.create_user(self.cleaned_data['username'],self.cleaned_data['email'],self.cleaned_data['password'])
    class Meta:
        model = User
        fields = ("username","password","email")

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    username = forms.CharField(required=False)
    def clean_username(self):
        u = self.cleaned_data['username']
        users = User.objects.filter(username=u)
        if users:
            if users[0] != self.instance.user:
                raise ValidationError("That username is already taken")
        return u
    def save(self,commit=True):
        instance = super(ProfileForm,self).save(commit=commit)

        u = instance.user
        u.username = self.cleaned_data['username']
        u.save()

        return instance
    class Meta:
        model = Profile
        exclude = ("user",)
