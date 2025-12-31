from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/like/", views.like_post, name="like_post"),
    path("post/<int:post_pk>/comment/<int:pk>/delete/", views.delete_comment, name="delete_comment"),
    path("category/<str:category_name>/", views.post_list, name="posts_by_category"),
    path("tag/<str:tag_name>/", views.tag_detail, name="posts_by_tag"),
    path("", views.post_list, name="post_list"),
]
