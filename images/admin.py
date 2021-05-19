from django.contrib import admin
from .models import Plan, Image, Profile, TempUrl


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan']


class TempUrlAdmin(admin.ModelAdmin):
    list_display = ['user', 'image_id', 'expiry']


admin.site.register(Plan)
admin.site.register(Image)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TempUrl, TempUrlAdmin)
