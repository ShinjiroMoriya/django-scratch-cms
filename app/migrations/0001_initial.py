# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-17 18:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(default=uuid.uuid4, editable=False, max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('contents', models.TextField()),
                ('status', models.CharField(default='draft', max_length=255)),
                ('publish_date', models.DateTimeField(default=datetime.datetime.now)),
                ('registration_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'post',
                'ordering': ['-publish_date'],
            },
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_id', models.CharField(max_length=255, unique=True)),
                ('image_url', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('registration_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'post_image',
                'ordering': ['-registration_date'],
            },
        ),
        migrations.CreateModel(
            name='PostPdf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_id', models.CharField(max_length=255, unique=True)),
                ('pdf_url', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('registration_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'post_pdf',
                'ordering': ['-registration_date'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='use_images',
            field=models.ManyToManyField(blank=True, related_name='post_image', to='app.PostImage'),
        ),
        migrations.AddField(
            model_name='post',
            name='use_pdfs',
            field=models.ManyToManyField(blank=True, related_name='post_pdf', to='app.PostPdf'),
        ),
    ]
