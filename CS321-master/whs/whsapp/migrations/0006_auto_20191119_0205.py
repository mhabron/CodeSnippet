# Generated by Django 2.2.6 on 2019-11-19 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whsapp', '0005_auto_20191117_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='event_logo',
            field=models.ImageField(blank=True, default='https://brand.gmu.edu/wp-content/uploads/assets/primarylogo/PC/GMURGB.jpg', upload_to='static/logos'),
        ),
    ]
