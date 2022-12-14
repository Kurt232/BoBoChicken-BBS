from django.urls import path, re_path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),#登录
    path('register', views.register, name="register"),#注册
    path('register_check', views.register_check, name="register_check"),#注册确认
    path('post', views.post, name="post"),#发帖
    path('post/star', views.star, name='star'),#收藏
    path('post/like', views.like, name='like'),#点赞
    path('reply', views.reply, name="reply"),#回复
    path('follow',views.follow, name='follow'), # follow
    path('post/seen', views.seen, name="seen"), # 浏览
    path('logout', views.logout, name="logout"),#登出
    path('search', views.search, name="search"),#搜索
    path('info', views.info, name="info"), # 用户信息
    path('info/post', views.get_post, name="get_post"), # 用户信息
    path('info/like', views.get_like, name="get_like"), # 用户信息
    path('info/star', views.get_star, name="get_star"), # 用户信息
    path('info/reply', views.get_reply, name="get_reply"), # 用户信息
    path('info/follow', views.get_follow, name="get_follow"), # 用户信息
    path('info/followed', views.get_followed, name="get_followed"), # 用户信息
    path('deleteBbs', views.deleteBbs, name="deleteBbs"), # 删帖
]
