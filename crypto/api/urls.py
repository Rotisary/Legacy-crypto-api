from django.urls import path

from crypto.api.views import get_price

urlpatterns = [
    path('price/', get_price, name='get-price')
] 