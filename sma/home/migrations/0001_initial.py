# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('zip', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user_token', models.CharField(max_length=255)),
                ('card_token', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='User_Card',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_id', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('card', models.CharField(max_length=255)),
                ('cb_global', models.CharField(max_length=255)),
                ('cb_groceries', models.CharField(max_length=255)),
                ('cb_wholesale_clubs', models.CharField(max_length=255)),
                ('cb_amazon', models.CharField(max_length=255, null=True)),
                ('cb_restaurants', models.CharField(max_length=255, null=True)),
                ('cb_gasoline', models.CharField(max_length=255, null=True)),
                ('cb_department_stores', models.CharField(max_length=255, null=True)),
                ('cb_fee', models.CharField(max_length=255, null=True)),
                ('cb_type', models.CharField(max_length=255, null=True)),
                ('cb_is_default', models.CharField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='User_Card_User_Id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User_Card_Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now=True)),
                ('card', models.ForeignKey(related_name='User_Card_Transaction_card', to='home.User_Card')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='cards',
            field=models.ManyToManyField(related_name='User_Cards', to='home.User_Card'),
        ),
    ]
