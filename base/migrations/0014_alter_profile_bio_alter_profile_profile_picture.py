# Generated by Django 4.1.5 on 2023-01-13 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='I have nothing interesting to say yet...', max_length=400),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='avatar.svg', upload_to='uploads'),
        ),
    ]