from django.contrib import admin
from django.conf.urls import url, include
from django.urls import path
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from users import views 
urlpatterns = [
    # path('register/', views.ajax, name='ajax-view'),
    path('register/', views.register, name='register'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
 ]