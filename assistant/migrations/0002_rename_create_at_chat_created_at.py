# Generated by Django 4.2.5 on 2023-10-05 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assistant', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
