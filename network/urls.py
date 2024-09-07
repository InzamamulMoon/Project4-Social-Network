
from django.conf import settings
from django.urls import include, path

from . import views

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("new_post", views.npost, name="new_post"),
    path("user_profile/<str:profile_user>", views.user_profile, name="user_profile"),
    path("follow/<int:user_id>", views.follow, name="following"),
    path("unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("following_page/<str:user>",views.following_page, name="follow_page"),
   

   # API Route
    path("like/<int:user_id>", views.like_post, name="liked_post"),
    path("authenticate/<int:post_id>", views.user_authentication, name="Authenticate"),
    path("edit/<int:post_id>", views.create_edit, name="create_edit"),
    path("edit_post/", views.recieve_edit, name="recieve_edit"),
    path("user_profile/edit/<int:post_id>", views.create_edit, name="recieve_edit"),
    path("user_profile/edit_post/", views.recieve_edit, name="recieve_edit"),
]
