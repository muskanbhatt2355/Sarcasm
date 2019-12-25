from django.urls import path
from .import views
from .views import Play

urlpatterns=[
	path('',views.home, name='game-home'),
	path('play',Play.as_view(), name='play'),
	path('prize',views.prize, name='prize'),
	path('forum',views.forum, name='forum'),
	path('instructions',views.instructions, name='instructions'),
	path('contacts', views.contacts, name='contacts'),
	path('bonus',views.Bonus.as_view(),name='bonus'),
]