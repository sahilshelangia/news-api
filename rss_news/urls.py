from django.contrib import admin
from django.urls import path,include
from .views import index,collectNews,listScrapedArticle
app_name='rss_news'
urlpatterns = [
    path('',index,name='index'),
    path('collect-news/',collectNews,name='collectNews'),
    path('list-news/',listScrapedArticle,name='listScrapedArticle')
]
