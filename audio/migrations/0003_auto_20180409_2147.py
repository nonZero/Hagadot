# Generated by Django 2.0.4 on 2018-04-09 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audio', '0002_track_bookmarks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='track',
            options={'verbose_name': 'track', 'verbose_name_plural': 'tracks'},
        ),
    ]
