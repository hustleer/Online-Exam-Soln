# Generated by Django 3.0.6 on 2020-08-31 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_auto_20200831_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='sub_title',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='title',
        ),
    ]
