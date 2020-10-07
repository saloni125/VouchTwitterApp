from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.top_tweets_list, name='top_tweets_list'),
    path('tweets/', views.user_tweets_list, name='user_tweets_list'),
    path('auth/', views.auth, name='auth'),
    path('logout/', views.sign_out, name='sign_out'),
    re_path(r'^callback/$', views.callback, name='auth_return'),
]