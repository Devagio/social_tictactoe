# Generated by Django 4.1.5 on 2023-01-11 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_results_options_alter_room_best_of'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created']},
        ),
    ]
