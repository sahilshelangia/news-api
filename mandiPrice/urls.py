from django.urls import path
from .views import index,scrapMandiPrice
app_name='mandiPrice'
urlpatterns = [
    path('',index,name='index'),
    path('scrap-mandi-price/',scrapMandiPrice,name='scrapMandiPrice'),
]
