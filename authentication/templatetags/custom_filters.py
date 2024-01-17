# custom_filters.py
from django import template
from ..models import ProfileInfo

register = template.Library()

@register.filter(name='is_followed_by_user')
def is_followed_by_user(post_user, user):
    """
    Check if the given user is in the list of users who are following the post_user.

    Args:
    - post_user: The user whose followers are being checked.
    - user: The user to check for following.

    Returns:
    - True if the user is followed by the post_user, False otherwise.
    """
    return ProfileInfo.objects.filter(user=post_user, followed_by__user=user).exists()

