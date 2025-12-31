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
            if request.user.is_authenticated:
                new_comment.author = request.user.username
            else:
                author_name = request.POST.get('author')
                if not author_name:
                    # You might want to handle this error more gracefully
                    return redirect(post.get_absolute_url())
                new_comment.author = author_name
            new_comment.save()
            return redirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()

    is_liked = False
    if request.user.is_authenticated:
        if post.likes.filter(id=request.user.id).exists():
            is_liked = True
    else:
        if pk in request.session.get('liked_posts', []):
            is_liked = True

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'is_liked': is_liked
    })

@require_POST
@login_required
def delete_comment(request, post_pk, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.username == comment.author:
        comment.delete()
    return redirect('blog:post_detail', pk=post_pk)

@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    else:
        liked_posts = request.session.get('liked_posts', [])
        if pk in liked_posts:
            liked_posts.remove(pk)
            if post.anonymous_likes > 0:
                post.anonymous_likes -= 1
        else:
            liked_posts.append(pk)
            post.anonymous_likes += 1
        request.session['liked_posts'] = liked_posts
        post.save()
    return redirect(post.get_absolute_url())