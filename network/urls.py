
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.create_post_view, name="create"),
    path("profile/<int:profile_id>", views.profile_view, name="profile"),
    path("follow/<int:profile_id>", views.follow_view, name="follow"),
    path("following/", views.following_view, name="following"),
    path("edit/<int:post_id>", views.edit_post_view, name="edit")
]
