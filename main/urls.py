from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('like/<int:quote_id>/', views.like_quote, name='like_quote'),
    path('dislike/<int:quote_id>/', views.dislike_quote, name='dislike_quote'),
]
