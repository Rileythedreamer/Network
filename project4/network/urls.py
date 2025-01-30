
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.create_new_post, name="new_post"),
    path("profile/<str:username>", views.profile_page, name="profile"),
    path("profile/<str:username>/followers", views.followers_posts_view, name="followers"),
    path("profile/<str:username>/followings", views.followings_posts_view, name="followings"),
    path("profile/<str:username>/follow", views.follow_view, name="follow"),
    path("profile/<str:username>/unfollow", views.unfollow_view, name="unfollow"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like_view, name="like"),
    path("unlike/<int:post_id>", views.unlike_view, name="unlike")
]
