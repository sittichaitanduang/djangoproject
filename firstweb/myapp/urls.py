from django.urls import path

from .views import About, AllProducts, Home, Register, login, logout, profile, product_detail

urlpatterns = [
    path('', Home, name='home'),
    path('about', About, name='about'),
    path('products', AllProducts, name='all-products'),
    path('products/', AllProducts, name='all-products-slash'),
    path('products/<int:product_id>/', product_detail, name='product-detail'),
    path('register', Register, name='register'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('profile', profile, name='profile'),
]