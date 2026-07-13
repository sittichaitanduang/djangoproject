from django.urls import path
from .views import AllProducts, Home, About,Register, login, logout, profile

urlpatterns = [
     path('', Home), #localhost:8000
    path('about',About, name='about'),
    path('products',AllProducts, name='all-products'),
    path('register', Register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('profile', profile, name='profile'),
]