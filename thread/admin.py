from django.contrib import admin
from .models import Thread, Follow, Comment, Like, Rethread


admin.site.register(Thread)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rethread)
