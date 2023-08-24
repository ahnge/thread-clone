from django.db import models
from django.contrib.auth.models import User


class Thread(models.Model):
    threader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thread")
    content = models.TextField(default="")
    likes_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    repost_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Thread: {self.content[:20]}"


class ThreadImage(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="image_thread"
    )
    image = models.ImageField(upload_to="thread_images/")

    def __str__(self):
        return f"Thread image of {self.thread.content[:20]}"


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

    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)
        # Update the like_count of the related Thread
        self.thread.likes_count = Like.objects.filter(thread=self.thread).count()
        self.thread.save()

    def __str__(self):
        return f"{self.user.username} liked {self.thread.content[:20]}"


class Repost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super(Repost, self).save(*args, **kwargs)
        # Update the repost_count of the related Thread
        self.thread.repost_count = Repost.objects.filter(thread=self.thread).count()
        self.thread.save()

    def __str__(self):
        return f"{self.user.username} reposted {self.thread.content[:20]}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField(default="")
    likes_count = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default=0)
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sub_comment",
    )

    class Meta:
        ordering = ["-created_at"]

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Check if this is a new comment or an existing one being updated
        is_new_comment = self._state.adding
        super(Comment, self).save(*args, **kwargs)

        if is_new_comment and not self.parent_comment:
            # Update the comment_count of the related Thread
            self.thread.comment_count = Comment.objects.filter(
                thread=self.thread, parent_comment=None
            ).count()
            self.thread.save()
        if is_new_comment and self.parent_comment:
            # Update the comment_count of the related parent comment
            self.parent_comment.comment_count = Comment.objects.filter(
                thread=self.thread, parent_comment=self.parent_comment
            ).count()
            self.parent_comment.save()

    def __str__(self):
        return f"Comment: {self.content[:20]}"


class CommentImage(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_image"
    )
    image = models.ImageField(upload_to="comment_images/")

    def __str__(self):
        return f"Comment image of {self.comment.content}"


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
