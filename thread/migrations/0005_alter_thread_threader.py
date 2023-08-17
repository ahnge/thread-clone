# Generated by Django 4.2.4 on 2023-08-17 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thread', '0004_alter_imagethread_thread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thread',
            name='threader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread', to=settings.AUTH_USER_MODEL),
        ),
    ]
