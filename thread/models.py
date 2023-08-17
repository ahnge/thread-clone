from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Thread(models.Model):
    threader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thread")
    content = models.TextField(default="")
    likes_count = models.PositiveIntegerField(default=0)
    rethread_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Thread by {self.threader.username} at {self.created_at}"


class ImageThread(models.Model):
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
        return f"{self.user.username} liked {self.thread.content_object}"


class Rethread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} rethreaded {self.thread}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.tweet}"


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
