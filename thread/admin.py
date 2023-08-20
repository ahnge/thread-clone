from django.contrib import admin
from .models import (
    Thread,
    ThreadImage,
    Follow,
    Comment,
    CommentImage,
    Like,
    Repost,
)


admin.site.register(Thread)
admin.site.register(ThreadImage)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(CommentImage)
admin.site.register(Like)
admin.site.register(Repost)
