# Generated by Django 2.1.7 on 2019-02-24 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tube', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='new_announcement',
            field=models.BooleanField(default=False),
        ),
    ]
