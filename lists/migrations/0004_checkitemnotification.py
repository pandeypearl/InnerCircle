# Generated by Django 4.2.5 on 2023-10-03 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0003_checkitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckItemNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('check_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.checkitem')),
                ('list_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.listitem')),
                ('list_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
