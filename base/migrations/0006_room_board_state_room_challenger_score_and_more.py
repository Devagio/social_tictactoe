# Generated by Django 4.1.5 on 2023-01-10 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_room_anon_viewers'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='board_state',
            field=models.CharField(default='.........', max_length=40),
        ),
        migrations.AddField(
            model_name='room',
            name='challenger_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='host_score',
            field=models.IntegerField(default=0),
        ),
    ]
