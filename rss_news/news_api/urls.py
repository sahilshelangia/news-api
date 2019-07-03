from django.contrib import admin
from django.urls import path,include
from .views import ArticleListAPIView,ArticleTitleListAPIView
app_name='rss_news_api'
urlpatterns = [
    path('list-news/',ArticleListAPIView.as_view(),name='ArticleListAPIView'),
    path('list-title-news/',ArticleTitleListAPIView.as_view(),name='ArticleTitleListAPIView'),
]
