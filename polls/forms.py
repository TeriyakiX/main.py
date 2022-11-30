from django import forms
from .models import Question, Choice
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class MyUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        exclude = ['user']

class ProfileFormWithoutHelpText(ProfileForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = 'аватар'
