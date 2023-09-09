from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (
    Like,
    LikeComment,
    Comment,
    Follow,
    Notification,
    Repost,
    RepostComment,
)


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


@receiver(post_save, sender=Like)
def create_notification_like_thread(sender, instance, **kwargs):
    """Create notification for like."""
    if not instance.thread.user == instance.user:
        Notification.objects.create(
            user=instance.thread.user,
            type="like_thread",
            content=f"{instance.user.username} likes your thread: {instance.thread.content[:20]}...",
            actioner=instance.user,
        )


@receiver(post_save, sender=LikeComment)
def create_notification_like_comment(sender, instance, **kwargs):
    """Create notification for likeComment."""
    if not instance.user == instance.comment.user:
        Notification.objects.create(
            user=instance.comment.user,
            type="like_comment",
            content=f"{instance.user.username} likes your comment: {instance.comment.content[:20]}...",
            actioner=instance.user,
        )


@receiver(post_save, sender=Repost)
def create_notification_repost_thread(sender, instance, **kwargs):
    """Create notification for Repost."""
    if not instance.user == instance.thread.user:
        Notification.objects.create(
            user=instance.thread.user,
            type="repost_thread",
            content=f"{instance.user.username} reposted your thread: {instance.thread.content[:20]}...",
            actioner=instance.user,
        )


@receiver(post_save, sender=RepostComment)
def create_notification_repost_comment(sender, instance, **kwargs):
    """Create notification for RepostComment."""
    if not instance.user == instance.comment.user:
        Notification.objects.create(
            user=instance.comment.user,
            type="repost_comment",
            content=f"{instance.user.username} reposted your comment: {instance.comment.content[:20]}...",
            actioner=instance.user,
        )


@receiver(post_save, sender=Follow)
def create_notification_follow(sender, instance, **kwargs):
    """Create notification for Follow."""
    Notification.objects.create(
        user=instance.followed,
        type="follow",
        content=f"{instance.follower.username} started following you.",
        actioner=instance.follower,
    )


@receiver(post_save, sender=Comment)
def create_notification_comment(sender, instance, **kwargs):
    """Create notification for Comment."""
    if instance.parent_comment:
        if not instance.parent_comment.user == instance.user:
            Notification.objects.create(
                user=instance.parent_comment.user,
                type="comment",
                content=f"{instance.user.username} reply to your comment: {instance.parent_comment.content[:20]}...",
                actioner=instance.user,
            )
    else:
        if not instance.thread.user == instance.user:
            Notification.objects.create(
                user=instance.thread.user,
                type="comment",
                content=f"{instance.user.username} reply to your thread: {instance.thread.content[:20]}...",
                actioner=instance.user,
            )
