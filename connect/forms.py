from django import forms
from django.contrib.auth.models import User
import re


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_username(self):
        cd = self.cleaned_data
        if cd['username'] in [user.username for user in User.objects.all()]:
            raise forms.ValidationError('Username is already taken.')
        return cd['username']

    def clean_email(self):
        cd = self.cleaned_data
        if not re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', cd['email']):
            raise forms.ValidationError('Please insert a valid email address.')
        return cd['email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class ResetPassword(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput())
    conf_password = forms.CharField(widget=forms.PasswordInput())

    def clean_conf_password(self):
        password = self.cleaned_data['password']
        conf_password = self.cleaned_data['conf_password']

        if password != conf_password:
            raise forms.ValidationError('Both password fields should match')
        else:
            return conf_password


class SearchProfileForm(forms.Form):
    query = forms.CharField()
