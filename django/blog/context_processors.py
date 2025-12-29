from .models import Category, Tag
from django.core.cache import cache

def all_categories(request):
    all_categories = cache.get('all_categories')
    if not all_categories:
        all_categories = Category.objects.all()
        cache.set('all_categories', all_categories, 900)  # Cache for 15 minutes
    return {
        'all_categories': all_categories
    }

def all_tags(request):
    all_tags = cache.get('all_tags')
    if not all_tags:
        all_tags = Tag.objects.all()
        cache.set('all_tags', all_tags, 900)  # Cache for 15 minutes
    return {
        'all_tags': all_tags
    }

