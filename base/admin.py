from django.contrib import admin

from .models import Room, Message, Results, Profile


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Results)
admin.site.register(Profile)
