# Generated by Django 3.0.6 on 2022-04-01 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_profile_test'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postrate',
            old_name='created_by',
            new_name='created_on',
        ),
    ]
