# Generated by Django 2.0 on 2017-12-11 20:10

from django.db import migrations, models


def fill_num_pages(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    for o in Book.objects.all():
        o.num_pages = o.pages.count()
        o.save()


class Migration(migrations.Migration):
    dependencies = [
        ('books', '0004_auto_20171211_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='num_pages',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.RunPython(fill_num_pages),
    ]
