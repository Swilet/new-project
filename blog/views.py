from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Category, Comment, Tag
from travel.models import Travel
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def post_list(request, category_name=None):
    search_query = request.GET.get('q', '')
    category = None
    post_list = Post.objects.all()

    if category_name:
        category = get_object_or_404(Category, name=category_name)
        post_list = post_list.filter(categories=category)
    
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

    travels = Travel.objects.all().order_by('-created_at')

    return render(request, "blog/post_list.html", {
        "posts": posts,
        "page": page,
        "category": category,
        "search_query": search_query,
        "travels": travels,
    })

def tag_detail(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag).prefetch_related('categories', 'tags').order_by("-created_at")
    travels = Travel.objects.filter(tags=tag).prefetch_related('tags').order_by('-created_at')

    return render(request, 'blog/tag_detail.html', {
        'tag': tag,
        'posts': posts,
        'travels': travels,
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
            new_comment.author = request.user.username 
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

@require_POST
@login_required
def delete_comment(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.username == comment.author:
        comment.delete()
    return redirect('blog:post_detail', pk=post_pk)

@login_required
@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(post.get_absolute_url())