from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)
    best_of = models.IntegerField(choices=[(i, str(i)) for i in range(1,7)], default=1)
    challenger = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='challenger', blank=True, default=None)
    overall = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='overall', blank=True)
    done = models.BooleanField(default=False)
    viewers = models.ManyToManyField(User, related_name='viewers')
    anon_viewers = models.IntegerField(default=0)
    board_state = models.CharField(max_length=40, default=".........")
    host_score = models.IntegerField(default=0)
    challenger_score = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.body[:40]


class Results(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.room.name


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    full_name = models.CharField(max_length=40, blank=False)
    profile_picture = models.ImageField(null=True, default='avatar.svg')
    bio = models.CharField(max_length=400, null=True, default="I have nothing interesting to say yet...")
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.full_name