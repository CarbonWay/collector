# Generated by Django 3.2.13 on 2022-07-01 09:35

from django.db import migrations, models
import django.utils.timezone
import loader.models


class Migration(migrations.Migration):

    dependencies = [
        ('loader', '0003_alter_device_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='datafile',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='datafile',
            name='file',
            field=models.FileField(upload_to=loader.models.user_directory_path),
        ),
    ]