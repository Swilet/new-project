from django import template
from ..models import Post
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('blog/partials/recent_posts.html')
def show_recent_posts(count=5):
    recent_posts = cache.get('recent_posts')
    if not recent_posts:
        recent_posts = Post.objects.prefetch_related('categories').order_by('-created_at')[:count]
        cache.set('recent_posts', recent_posts, 300)  # Cache for 5 minutes
    return {'recent_posts': recent_posts}
