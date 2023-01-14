from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Room, Profile


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('host', 'viewers', 'anon_viewers', 'board_state', 'host_score', 'challenger_score', 'overall', 'done', 'challenger',)
        

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username',)


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'wins', 'draws', 'losses',)