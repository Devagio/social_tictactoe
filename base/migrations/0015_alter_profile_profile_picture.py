# Generated by Django 4.1.5 on 2023-01-13 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_profile_bio_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='avatar.svg', upload_to=''),
        ),
    ]
