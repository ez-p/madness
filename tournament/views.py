"""
Copyright 2016, Paul Powell, All rights reserved.
"""
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
import django.views.generic as generic

import tournament.engine.tourney as tourney
from tournament.forms import UserForm, OptionsForm, RegistrationForm, LoginForm
import tournament.models as models
from tournament.engine.algorithms.seedodds import SeedOddsMatchup as algorithm

class RegisterView(generic.CreateView):
    form_class = RegistrationForm 
    model = User
    success_url = reverse_lazy('home-page')
    template_name = 'registration/register.html'

    def form_valid(self,form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        # This should log in the user but it doesn't???
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)

class LoginView(generic.FormView):
    form_class = LoginForm
    success_url = reverse_lazy('home-page')
    template_name = 'registration/login.html'

    def form_valid(self,form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

def _save_region_rounds(eng_results, region):
    year = models.Year.objects.get(year=eng_results['year'])
    for round in eng_results[region.name].rounds:
        new_round = models.Round(region=region)    
        new_round.save()
       
        teams = models.Team.objects.filter(year=year)

        for matchup in round.results:
            winner = teams.get(name=matchup.winner.name)
            loser = teams.get(name=matchup.loser.name)
            m = models.Matchup(team1=winner, team2=loser, winner=winner)
            m.round = new_round
            m.save()

# Save tournament results generated by engine
def _save_tournament(eng_results, option_id=None):
    options = None
    year = models.Year.objects.get(year=eng_results['year'])
    if not option_id:
        algorithm = models.Algorithm.objects.get(name="Seed Odds")
        options = models.Options()
        options.algorithm = algorithm
        options.year = year
        options.save()
    else:
        options = models.Options.objects.get(id=option_id)

    teams = models.Team.objects.filter(year=year)

    # Store the resuls in the database
    tourney = models.Tournament()
    tourney.year = year
    tourney.winner = teams.get(name=eng_results['champion'].name)
    tourney.runnerup = teams.get(name=eng_results['2nd_place'].name)
    tourney.upsets = eng_results['upsets']
    tourney.options = options
    tourney.save()

    semi1 = models.Matchup()
    semi1.team1=teams.get(name=eng_results['semi1'].winner.name)
    semi1.team2=teams.get(name=eng_results['semi1'].loser.name)
    semi1.winner=semi1.team1
    semi1.tournament = tourney
    semi1.save()

    semi2 = models.Matchup()
    semi2.team1=teams.get(name=eng_results['semi2'].winner.name)
    semi2.team2=teams.get(name=eng_results['semi2'].loser.name)
    semi2.winner=semi2.team1
    semi2.tournament = tourney
    semi2.save()

    tourney.semis.add(semi1, semi2)

    for rdata in models.RegionData.objects.filter(year=year):
        region = models.Region()
        region.name = rdata.name
        region.tournament = tourney
        region.save()
        _save_region_rounds(eng_results, region)

    return tourney.id

def _get_default_year(request):
    year = None
    year_cookie = request.COOKIES.get('year')
    if not year_cookie:
        return models.Year.objects.get(year=settings.DEFAULT_YEAR)
    else:
        return models.Year.objects.get(year=year_cookie)

def home_page(request):
    year = _get_default_year(request)
    context = {'year':year.year}
    return render(request, 'index.html', context)

def run_tournament(request):
    # Engine generated tournament object (not from models.py)
    year_s = str(_get_default_year(request))
    t = tourney.Tournament(year_s, None, None, 1, algorithm)
    _results = t()

    # Store the resuls in the database
    db_tourney_id = _save_tournament(_results)

    return redirect('view-result', result_id=db_tourney_id)

def run_tournament_options(request, option_id):
    options = models.Options.objects.get(id=option_id)
    winner_name = None
    second_name = None

    if options.winner:
        winner_name = options.winner.name

    if options.second:
        second_name = options.second.name

    from tournament.engine.algorithms.seedodds import SeedOddsMatchup as algorithm

    if options.algorithm.name == "Fifty Fifty":
        from tournament.engine.algorithms.fiftyfifty import FiftyFifty as algorithm
    # Engine generated tournament object (not from models.py)
    t = tourney.Tournament(options.year, winner_name, second_name, options.madness, algorithm)
    _results = t()

    # Store the resuls in the database
    db_tourney_id = _save_tournament(_results, option_id)

    return redirect('view-result', result_id=db_tourney_id)

@login_required
def save_result(request, result_id):
    _result = models.Tournament.objects.get(id=result_id)
    _result.user = request.user
    _result.save()

    return redirect('view-result', result_id=result_id)

def remove_result(request, result_id):
    _result = models.Tournament.objects.get(id=result_id)
    _result.user = None
    _result.save()

    return redirect('my-brackets')

def _view_base_results(request, result_id):
    tourney = models.Tournament.objects.get(id=result_id)

    # Return result information to the template
    results = {'tourney':tourney,
               'semi1':tourney.semis.all()[0],
               'semi2':tourney.semis.all()[1],
               'is_saved':False,
               }

    if request.user.is_authenticated():
        if request.user.tournament_set.filter(id=result_id):
            results['is_saved'] = True

    for r in tourney.region_set.all():
        results[r.name] = r

    return results

def view_result(request, result_id):
    results = _view_base_results(request, result_id)
    # Specifies layout of rounds for pretty display
    results['is_full'] = False
    return render(request, 'view.html', results)

def view_full_result(request, result_id):
    results = _view_base_results(request, result_id)

    t = results['tourney']
    year = t.year

    results['is_full'] = True 
    # Specify order the rounds are printed in the full tourney view
    results['order'] = [8,4,2,1]
    results['r_order'] = list(reversed(results['order']))

    semi1_regions = []
    semi1_regions.append(results['semi1'].winner.region.name)
    semi1_regions.append(results['semi1'].loser.region.name)
    results['semi1_regions'] = (t.region_set.get(name=semi1_regions[0]),
                                t.region_set.get(name=semi1_regions[1]))

    semi2_regions = []
    semi2_regions.append(results['semi2'].winner.region.name)
    semi2_regions.append(results['semi2'].loser.region.name)
    results['semi2_regions'] = (t.region_set.get(name=semi2_regions[0]),
                                t.region_set.get(name=semi2_regions[1]))
    return render(request, 'view_full.html', results)

@login_required
def my_brackets(request):
    context = {'user':request.user}
    return render(request, 'my_brackets.html', context)

def _create_with_options_impl(request, year):
    years = models.Year.objects.all()
    if request.method == "POST":
        form = OptionsForm(request.POST, year=year)
        if not form.is_valid():
            return render(request, 'options.html', {'form':form, 'years':years})
        options = form.save()
        return redirect('run-tournament-options', option_id=options.id)
    else:
        algorithm = models.Algorithm.objects.get(name="Seed Odds")
        initial={'algorithm':algorithm, 'year':year}
        form = OptionsForm(initial=initial, year=year)
        return render(request, 'options.html', {'form':form, 'year':year, 'years':years})

def create_with_options(request):
    year = _get_default_year(request)
    return _create_with_options_impl(request, year)

def create_with_options_year(request, year):
    year = models.Year.objects.get(year=year)
    rsp =_create_with_options_impl(request, year)
    rsp.set_cookie('year',year.year)
    return rsp

def help_introduction(request):
    return render(request, 'help_intro.html')

def help_save(request):
    return render(request, 'help_save.html')

def help_create(request):
    return render(request, 'help_create.html')

def help_show(request):
    return render(request, 'help_show.html')

def print_bracket(request):
    return render(request, 'ok')
