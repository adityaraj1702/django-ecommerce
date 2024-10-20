from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartProducts, Seller, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, ProductForm

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def test(request):
    products = Product.objects.all()
    return render(request, 'test.html',{'products':products})

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, "Logged in succesfully!")
            return redirect('home')
        else:
            #messages.success(request, "Invalid credentials!")
            return redirect('login')
    else:
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    #messages.success(request,("Logged out successfully!"))
    return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'product':product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_product, created = CartProducts.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_product.quantity += 1
        cart_product.save()

    return redirect('cart_page')

def cart_page(request):
    cart = Cart.objects.filter(user=request.user).first()
    cart_products = CartProducts.objects.filter(cart=cart) if cart else []
    return render(request, 'cart.html', {'cart_products': cart_products})

def register(request):
    if request.method == 'POST':
        #print('hello')
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def seller_page(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            seller = Seller.objects.get(user=request.user)
            product.seller = seller
            product.save()
            return redirect('seller_page')
    else:
        form = ProductForm()
    
    seller = Seller.objects.get(user=request.user)
    seller_products = Product.objects.filter(seller=seller)
    
    # Fetch all categories to pass to the template
    categories = Category.objects.all()
    
    return render(request, 'seller.html', {'form': form, 'products': seller_products, 'categories': categories})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_page')
    else:
        form = ProductForm(instance=product)
    
    # Fetch all categories to pass to the template
    categories = Category.objects.all()

    return render(request, 'edit_product.html', {'form': form, 'product': product, 'categories': categories})


