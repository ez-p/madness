"""
Copyright 2016, Paul Powell, All rights reserved.
"""
from django.contrib import admin
import tournament.models as models

# Register your models here.
admin.site.register(models.Year)
admin.site.register(models.RegionData)
admin.site.register(models.Team)
admin.site.register(models.Algorithm)
admin.site.register(models.Options)
admin.site.register(models.Tournament)
admin.site.register(models.Region)
admin.site.register(models.Round)
admin.site.register(models.Matchup)
