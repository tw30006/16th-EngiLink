from django.contrib import admin
from .models import Profile
from .forms import ProfileForm


class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    exclude = ['deleted_at','created_at']
    radio_fields = {'gender': admin.HORIZONTAL, 'experience': admin.HORIZONTAL}

admin.site.register(Profile, ProfileAdmin)
