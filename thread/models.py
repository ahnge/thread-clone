from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    threader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thread")
    content = models.TextField(default="")
    likes_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Thread by {self.threader.username} at {self.created_at}"


class ThreadImage(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="image_thread"
    )
    image = models.ImageField(upload_to="thread_images/")

    def __str__(self):
        return f"Thread image by {self.thread.threader.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ensures a user can only like a thread once
        constraints = [
            models.UniqueConstraint(fields=["user", "thread"], name="unique_like")
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.thread.content[:10]}"


class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} rethreaded {self.thread.content[:10]}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField(default="")
    likes_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.thread.threader.username}'s post."


class CommentImage(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_image"
    )
    image = models.ImageField(upload_to="comment_images/")

    def __str__(self):
        return f"Comment image by {self.comment.user.username}"


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

    class Meta:
        # Ensures that a user can only follow another user once.
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followed"], name="unique_following"
            )
        ]
