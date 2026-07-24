from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Brand, Category, Product as ShopProduct

from .forms import UserRegisterForm
from .models import Profile


# Create your views here.
def Home(request):
    return render(request, 'home.html')


def About(request):
    return render(request, 'about.html')


def AllProducts(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'name')

    products = ShopProduct.objects.select_related('brand', 'category')

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    if sort_by == 'price_low_to_high':
        products = products.order_by('price', 'name')
    elif sort_by == 'price_high_to_low':
        products = products.order_by('-price', 'name')
    else:
        products = products.order_by('name')

    categories = Category.objects.all().order_by('name')
    context = {
        'products': products,
        'categories': categories,
        'active_category': category_id,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'allproducts.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(ShopProduct, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def Register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'ยินดีต้อนรับ {username} บัญชีของคุณถูกสร้างแล้ว!')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('all-products')
        else:
            messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)
    return render(request, 'profile.html')
