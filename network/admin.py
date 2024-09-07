from django.contrib import admin
from .models import User,NPost_model,Profile

# Register your models here.

admin.site.register(User)
admin.site.register(NPost_model)
admin.site.register(Profile)
