# Generated by Django 3.0.6 on 2020-08-31 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_banner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banner',
            old_name='Title',
            new_name='title',
        ),
    ]