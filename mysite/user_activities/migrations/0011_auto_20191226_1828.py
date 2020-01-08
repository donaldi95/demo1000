# Generated by Django 2.1.7 on 2019-12-26 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_activities', '0010_auto_20191218_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='peak_annotations',
            name='localized_names',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='peak_annotations',
            name='provenance_org',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]