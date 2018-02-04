# Generated by Django 2.0 on 2018-01-28 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20180115_0844'),
    ]

    operations = [
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.DecimalField(decimal_places=1, max_digits=5)),
                ('y', models.DecimalField(decimal_places=1, max_digits=5)),
                ('content', models.TextField(verbose_name='content')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='annotations', to='books.Page')),
            ],
        ),
    ]