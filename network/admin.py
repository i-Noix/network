from django.contrib import admin
from .models import User, Like, Posts

# Register your models here.
admin.site.register(User)
admin.site.register(Like)
admin.site.register(Posts)