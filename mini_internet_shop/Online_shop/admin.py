from django.contrib import admin

from .forms import UserProfile

admin.site.register([UserProfile])