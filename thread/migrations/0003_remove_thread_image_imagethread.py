# Generated by Django 4.2.4 on 2023-08-09 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('thread', '0002_delete_imagethread_delete_textthread_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='image',
        ),
        migrations.CreateModel(
            name='ImageThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='thread_images/')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thread.thread')),
            ],
        ),
    ]
