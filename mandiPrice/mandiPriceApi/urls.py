from django.contrib import admin
from django.urls import path,include
from .views import MandiPriceApiView
app_name='mandiPriceApi'
urlpatterns = [
    path('mandi-price-api/',MandiPriceApiView.as_view(),name='MandiPriceApiView'),
]
