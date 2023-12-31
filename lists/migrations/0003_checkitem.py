# Generated by Django 4.2.5 on 2023-09-27 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0002_remove_member_phone_number'),
        ('lists', '0002_listitem_checked_delete_checkeditem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_at', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.listitem')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circle.member')),
            ],
        ),
    ]
