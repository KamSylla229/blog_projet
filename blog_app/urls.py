from django.contrib import admin
from django.urls import path, include
from . import views
from .views import register_view, login_view, logout_view
from django.contrib.auth import views as auth_views

# urlpatterns = [
#     path('register/', register_view, name='register'),
#     path('login/', login_view, name='login'),
#     path('logout/', logout_view, name='logout'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('article/new/', views.article_create, name='article_create'),
    path('article/<int:pk>/edit/', views.article_update, name='article_update'),
    path('article/<int:pk>/delete/', views.article_delete, name='article_delete'),

    # Inscription personnalisée
    path('register/', views.register_view, name='register'),
]

