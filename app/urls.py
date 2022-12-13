from django.urls import path, re_path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name="register"),
    path('register_check', views.register_check, name="register_check"),
    path('post', views.post, name="post"),
    path('post/star', views.star, name='star'),
    path('reply', views.reply, name="reply"),
    # path('post/id?<int:post_id>', views.get_post, name="get_post"),
    path('logout', views.logout, name="logout"),
    # path('browsepost', views.browsepost, name="browsepost"),
]
