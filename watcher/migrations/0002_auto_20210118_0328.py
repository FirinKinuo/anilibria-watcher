# Generated by Django 3.1.5 on 2021-01-18 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watcher', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anime',
            name='anilibria_link',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='season',
        ),
        migrations.DeleteModel(
            name='Season',
        ),
    ]
