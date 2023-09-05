# Generated by Django 4.2.4 on 2023-09-05 04:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thread', '0016_thread_reposted_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='repost_count',
        ),
        migrations.CreateModel(
            name='RepostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='thread.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='reposted_users',
            field=models.ManyToManyField(blank=True, related_name='reposted_comments', through='thread.RepostComment', to=settings.AUTH_USER_MODEL),
        ),
    ]