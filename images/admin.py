from django.contrib import admin
from .models import Plan, Image, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan']


admin.site.register(Plan)
admin.site.register(Image)
admin.site.register(Profile, ProfileAdmin)
