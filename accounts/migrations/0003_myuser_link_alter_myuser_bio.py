# Generated by Django 4.2.4 on 2023-08-17 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_myuser_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='link',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='bio',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
