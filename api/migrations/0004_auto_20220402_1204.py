# Generated by Django 3.0.6 on 2022-04-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20220401_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postrate',
            name='created_on',
            field=models.DateField(auto_now=True),
        ),
    ]