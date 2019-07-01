from django.contrib import admin
from django.urls import path,include
from .views import ArticleListAPIView
urlpatterns = [
    path('list-news/',ArticleListAPIView.as_view(),name='ArticleListAPIView')
]
