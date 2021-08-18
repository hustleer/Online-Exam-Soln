# Generated by Django 3.0.6 on 2020-08-22 08:29

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('message', models.TextField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('New', 'New'), ('Read', 'Read'), ('Closed', 'Closed')], default='New', max_length=10)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('note', models.CharField(blank=True, max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(blank=True, choices=[('en', 'English'), ('tr', 'Türkçe')], max_length=6, null=True)),
                ('ordernumber', models.IntegerField()),
                ('question', models.CharField(max_length=200)),
                ('answer', ckeditor_uploader.fields.RichTextUploadingField()),
                ('status', models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=5)),
                ('status', models.BooleanField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=50)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('fax', models.CharField(blank=True, max_length=15)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('smtpserver', models.CharField(blank=True, max_length=50)),
                ('smtpemail', models.CharField(blank=True, max_length=50)),
                ('smtppassword', models.CharField(blank=True, max_length=10)),
                ('smtpport', models.CharField(blank=True, max_length=5)),
                ('icon', models.ImageField(blank=True, upload_to='images/')),
                ('facebook', models.CharField(blank=True, max_length=50)),
                ('instagram', models.CharField(blank=True, max_length=50)),
                ('twitter', models.CharField(blank=True, max_length=50)),
                ('youtube', models.CharField(blank=True, max_length=50)),
                ('aboutus', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('contact', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('references', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('status', models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=10)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SettingLang',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('en', 'English'), ('tr', 'Türkçe')], max_length=6)),
                ('title', models.CharField(max_length=150)),
                ('keywords', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('aboutus', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('contact', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('references', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Setting')),
            ],
        ),
    ]
