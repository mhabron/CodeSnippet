# Generated by Django 2.2.6 on 2019-11-18 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whsapp', '0004_auto_20191114_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='event_logo',
            field=models.ImageField(null=True, upload_to='static/logos'),
        ),
    ]
