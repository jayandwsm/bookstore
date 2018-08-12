# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-07-30 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookname', models.CharField(max_length=50, verbose_name='书名')),
                ('bookprice', models.DecimalField(decimal_places=2, max_digits=8)),
                ('bookdetail', models.CharField(max_length=100, verbose_name='图书细节')),
                ('bookdesc', models.CharField(max_length=200, verbose_name='图书描述')),
                ('bookpicture', models.ImageField(default='1.jpg', upload_to='static/images/books', verbose_name='实物')),
                ('bookunit', models.CharField(max_length=30, verbose_name='单位')),
                ('isdelete', models.BooleanField(default=False, verbose_name='删除')),
            ],
        ),
        migrations.CreateModel(
            name='BookType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typename', models.CharField(max_length=50, verbose_name='分类名')),
                ('typedesc', models.CharField(default='类型描述', max_length=100, verbose_name='描述')),
                ('isdelete', models.BooleanField(default=False, verbose_name='删除')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booksInfo.BookType'),
        ),
    ]