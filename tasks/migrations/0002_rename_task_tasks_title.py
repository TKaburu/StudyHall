# Generated by Django 5.0.3 on 2024-03-23 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasks',
            old_name='task',
            new_name='title',
        ),
    ]
