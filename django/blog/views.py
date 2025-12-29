from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Category, Comment, Tag
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request, category_name=None, tag_name=None):
    search_query = request.GET.get('q', '')
    category = None
    tag = None
    post_list = Post.objects.all()

    if category_name:
        category = get_object_or_404(Category, name=category_name)
        post_list = post_list.filter(categories=category)
    
    if tag_name:
        tag = get_object_or_404(Tag, name=tag_name)
        post_list = post_list.filter(tags=tag)
    
    if search_query:
        post_list = post_list.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        ).distinct()

    post_list = post_list.prefetch_related('categories', 'tags').order_by("-created_at")

    paginator = Paginator(post_list, 5) # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post_list.html", {
        "posts": posts,
        "page": page,
        "category": category,
        "tag": tag,
        "search_query": search_query,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.prefetch_related('categories', 'tags', 'comments'), pk=pk)
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)
        post.likes += 1
        post.save()
    return redirect(post.get_absolute_url())