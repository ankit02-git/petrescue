from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-request/', views.add_request, name='add_request'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('all-pets/', views.all_pets, name='all_pets'),
    path('favorites/', views.favorites, name='favorites'),
    path('pet/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('favorite/add/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    
]

