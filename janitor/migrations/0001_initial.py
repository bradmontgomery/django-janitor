# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 21:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldSanitizer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(help_text='The name of a field in the selected Model. It probably should be a TextField or some sublcass of TextField.', max_length=255)),
                ('tags', models.TextField(blank=True, default='a, abbr, acronym, blockquote, cite, code, dd, del, dfn, dl, dt, em, h1, h2, h3, h4, h5, h6, hr, img, ins, kbd, li, ol, p, pre, q, samp, strong, ul', help_text='A comma-separated whitelist of HTML tags that are allowed in the selected field')),
                ('attributes', models.TextField(blank=True, default='alt, class, href, id, src, title', help_text='A comma-separated whitelist of attributes that are allowed in the selected field')),
                ('styles', models.TextField(blank=True, help_text="A comma-separated whitelist of allowed CSS properties within a style attribute. NOTE: For this to work, 'style' must be in the list of attributes.")),
                ('strip', models.BooleanField(default=False, help_text='Strip disallowed HTML instead of escaping it.')),
                ('strip_comments', models.BooleanField(default=True, help_text='Strip HTML comments.')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['content_type', 'field_name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='fieldsanitizer',
            unique_together=set([('content_type', 'field_name')]),
        ),
    ]
