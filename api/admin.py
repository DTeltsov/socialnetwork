from django.contrib import admin
from .models import Post, PostRate, Profile

admin.site.register([Post, PostRate, Profile])

# Register your models here.
