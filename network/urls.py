
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_newPost", views.create_newPost, name="create_newPost"),
    path("profile/<int:user_id>", views.profile, name="profile"),


]
