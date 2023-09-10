# Generated by Django 4.2.4 on 2023-09-08 15:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('thread', '0017_remove_thread_repost_count_repostcomment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
                ('content', models.CharField(max_length=64)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='like',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='likecomment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddConstraint(
            model_name='repost',
            constraint=models.UniqueConstraint(fields=('user', 'thread'), name='unique_repost_thread'),
        ),
        migrations.AddConstraint(
            model_name='repostcomment',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='unique_repost_comment'),
        ),
        migrations.AddField(
            model_name='notification',
            name='actioner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='noti', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL),
        ),
    ]