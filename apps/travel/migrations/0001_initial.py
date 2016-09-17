# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-17 21:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('plan', models.TextField(max_length=500)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('travel_image', models.ImageField(blank=True, default='user/no.jpg', null=True, upload_to='travel/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=45)),
                ('pw_hash', models.CharField(max_length=255)),
                ('user_image', models.ImageField(blank=True, default='user/anonym.jpg', null=True, upload_to='user/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='travel',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='travel_create', to='travel.User'),
        ),
        migrations.AddField(
            model_name='join',
            name='travel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_travel', to='travel.Travel'),
        ),
        migrations.AddField(
            model_name='join',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_user', to='travel.User'),
        ),
    ]
