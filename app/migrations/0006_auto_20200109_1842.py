# Generated by Django 3.0.1 on 2020-01-09 18:42

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20200109_1835'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='recipe',
            name='app_recipe_search__7e0f6e_gin',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='search_vector',
            new_name='search',
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search'], name='app_recipe_search_0d6bb5_gin'),
        ),
    ]
