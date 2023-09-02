from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Like, LikeComment, Repost, Comment


@receiver(post_delete, sender=Like)
def update_likes_count(sender, instance, **kwargs):
    # Update the likes_count of the related Thread when a Like is deleted
    instance.thread.likes_count = Like.objects.filter(thread=instance.thread).count()
    instance.thread.save()


@receiver(post_delete, sender=LikeComment)
def update_cmt_likes_count(sender, instance, **kwargs):
    # Update the likes_count of the related comment when a Like is deleted
    instance.comment.likes_count = LikeComment.objects.filter(
        comment=instance.comment
    ).count()
    instance.comment.save()


@receiver(post_delete, sender=Repost)
def update_repost_count(sender, instance, **kwargs):
    # Update the repost_count of the related Thread when a Repost is deleted
    instance.thread.repost_count = Repost.objects.filter(thread=instance.thread).count()
    instance.thread.save()


@receiver(post_delete, sender=Comment)
def update_comment_count(sender, instance, **kwargs):
    # Update the comment_count of the related Thread when a parent_comment is deleted
    if not instance.parent_comment:
        instance.thread.comment_count = Comment.objects.filter(
            thread=instance.thread, parent_comment=None
        ).count()
        instance.thread.save()
    # Update the comment_count of the parent_comment
    else:
        instance.parent_comment.comment_count = Comment.objects.filter(
            thread=instance.thread, parent_comment=instance.parent_comment
        )
