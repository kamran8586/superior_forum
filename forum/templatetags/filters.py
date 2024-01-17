# custom_filters.py
from django import template

register = template.Library()
@register.filter(name='is_liked_by_user')
def is_liked_by_user(post, user):
    """
    Check if the given user has liked the post.

    Args:
    - post: The post to check for likes.
    - user: The user to check for liking.

    Returns:
    - True if the user has liked the post, False otherwise.
    """
    return post.likes.filter(user=user).exists()