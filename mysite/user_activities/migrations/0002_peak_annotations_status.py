# Generated by Django 2.1.7 on 2019-12-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_activities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='peak_annotations',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]