# Generated by Django 4.1.5 on 2023-01-10 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_viewers'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='anon_viewers',
            field=models.IntegerField(default=0),
        ),
    ]
