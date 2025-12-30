from django.urls import path
from . import views

app_name = 'travel'
urlpatterns = [
    path('', views.travel_list, name='travel_list'),
    path('travel/<int:pk>/', views.travel_detail, name='travel_detail'),
]
