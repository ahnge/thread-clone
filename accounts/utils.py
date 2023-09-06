from thread.models import Follow


def check_following(follower, followed):
    try:
        follow = Follow.objects.get(follower=follower, followed=followed)
        return True
    except Follow.DoesNotExist:
        return False
