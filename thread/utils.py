from .models import Thread, ThreadImage, Comment, CommentImage


def create_thread_post(content, user):
    thread = Thread(content=content)
    thread.user = user
    thread.save()
    return thread


def create_thread_images(image_list, thread):
    for img in image_list:
        thread_image = ThreadImage(thread=thread, image=img)
        thread_image.save()


def create_cmt(content, user, thread):
    comment = Comment(content=content)
    comment.user = user
    comment.thread = thread
    comment.save()
    return comment


def create_cmt_images(image_list, comment):
    for img in image_list:
        cmt_img = CommentImage(comment=comment, image=img)
        cmt_img.save()


def create_child_cmt(content, user, thread, parent_comment):
    comment = Comment(content=content)
    comment.user = user
    comment.thread = thread
    comment.parent_comment = parent_comment
    comment.save()
    return comment
