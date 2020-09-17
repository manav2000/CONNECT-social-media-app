from django import forms
from django.forms.widgets import Select

from .models import Profile
from django.contrib.auth.models import User

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
    ('Perfer Not To Say', 'Perfer Not To Say'),
)


class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    gender = forms.ChoiceField(choices=GENDER)

    class Meta():
        model = Profile
        fields = ('first_name', 'last_name', 'bio',
                  'gender', 'country', 'avatar')
