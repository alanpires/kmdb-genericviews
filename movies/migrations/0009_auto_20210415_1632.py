# Generated by Django 3.2 on 2021-04-15 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_auto_20210415_1414'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='criticism',
            old_name='user_id',
            new_name='critic',
        ),
    ]
