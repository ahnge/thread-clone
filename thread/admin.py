from django.contrib import admin
from .models import Thread, TextThread, ImageThread, Follow, Comment, Like, Rethread


admin.site.register(Thread)
admin.site.register(TextThread)
admin.site.register(ImageThread)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rethread)
