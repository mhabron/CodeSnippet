from django.conf.urls import url   
from django.urls import path
from . import views
from .views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='whsapp-home'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout, name = 'logout'),
    path('signup/', views.signup, name = 'signup'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
	path('post/new/', views.post_new, name='post_new'),
	path('test.txt', views.test, name='test'),
]
