"""
Copyright 2016, Paul Powell, All rights reserved.
"""
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.conf import settings
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

import tournament.models as models
import tournament.engine.data as data

class OptionsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        year = kwargs.pop('year')
        super(OptionsForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})

        #import pdb; pdb.set_trace()
        # HACK eventually year should be a selectable option
        self.year = models.Year.objects.get(year=year)
        teams = models.Team.objects.filter(year=self.year)
        self.fields['winner'].queryset = teams.order_by('region', 'name')
        self.fields['second'].queryset = teams.order_by('region', 'name')
    
    def _find_region(self, year, name):
        all_regions_cache = data.all_regions(year)
        for region in all_regions_cache:
            names = []
            for entry in all_regions_cache[region].values():
                names.append(entry['name'])
            if name in names:
                return region

    def _possible_matchup(self, year, winner, second):
        w_region = self._find_region(year, winner.name)
        s_region = self._find_region(year, second.name)

        if w_region == s_region:
            d = "{}".format(w_region.capitalize())
            s = "Selected teams cannot be in the same region. {} and {} are in the {} region."
            return s.format(winner.name, second.name, d)

        if data.exclusives(year)[w_region] == s_region:
            d = "({}, {})".format(w_region.capitalize(), s_region.capitalize())
            s = "{} and {} cannot play each other in the championship.\nThey are from mutually exclusive regions {}"
            return s.format(winner.name, second.name,d)

        return None

    def clean(self):
        cleaned_data = super(OptionsForm, self).clean()
        winner = cleaned_data.get("winner")
        second = cleaned_data.get("second")

        if winner and second:
            e_str = self._possible_matchup(self.year, winner, second)
            if e_str:
                raise forms.ValidationError(e_str)

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
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            ButtonHolder(
                Submit('login', 'Login', css_class='btn-primary')
            )
        )

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
