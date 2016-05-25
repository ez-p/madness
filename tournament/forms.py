"""
Copyright 2016, Paul Powell, All rights reserved.
"""
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

import tournament.models as models

class OptionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OptionsForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})

        year = models.Year.objects.get(year=settings.DEFAULT_YEAR)
        teams = models.Team.objects.filter(year=year)
        self.fields['winner'].queryset = teams.order_by('name')
        self.fields['second'].queryset = teams.order_by('name')

    class Meta:
        model = models.Options
        fields = ('madness', 'winner', 'second', 'algorithm')

class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            ButtonHolder(
                Submit('register', 'Register', css_class='btn-primary')
            )
        )

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
