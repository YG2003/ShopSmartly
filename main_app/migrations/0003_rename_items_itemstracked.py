# Generated by Django 4.2 on 2023-04-29 04:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0002_items_desired_price'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='items',
            new_name='ItemsTracked',
        ),
    ]
