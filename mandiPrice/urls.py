from django.urls import path
from .views import index
app_name='mandiPrice'
urlpatterns = [
    path('',index,name='index'),
]
