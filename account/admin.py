from django.contrib import admin

from account.models import Profile, Algorithm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'code')


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    fields = ('user', 'name', 'params', 'slug', 'image', 'file', 'status')
