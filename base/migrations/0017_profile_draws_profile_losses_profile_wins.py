# Generated by Django 4.1.5 on 2023-01-13 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_alter_profile_bio_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='draws',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
