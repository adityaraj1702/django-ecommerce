from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, CartProducts, Seller, Category, Order, OrdersProducts, UserOrders, UserProfile, UserAddresses, Address
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import CustomUserCreationForm, ProductForm

def home(request):
    products = Product.objects.all()
    
    # Check if the user is a seller
    is_seller = False
    if request.user.is_authenticated:
        is_seller = Seller.objects.filter(user=request.user).exists()

    return render(request, 'home.html', {'products': products, 'is_seller': is_seller})


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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will save the user and associated profile and address
            login(request, user)  
            return redirect('home') 
        else:
            messages.error(request, 'Please correct the errors below.')
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
        # Check if the delete button was clicked
        if 'delete' in request.POST:
            product.delete()
            return redirect('seller_page')
        
        # Otherwise, handle the update functionality
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_page')
    else:
        form = ProductForm(instance=product)

    categories = Category.objects.all()

    return render(request, 'edit_product.html', {'form': form, 'product': product, 'categories': categories})

#@login_required
def checkout(request):
    # Retrieve user's cart
    cart = Cart.objects.get(user=request.user)
    cart_products = CartProducts.objects.filter(cart=cart)

    # Calculate total order amount
    order_total = sum(item.quantity * item.product.product_price for item in cart_products)

    # Create a new order
    order = Order.objects.create(order_total=order_total, date=timezone.now(), status=False)

    # Link products from the cart to the order and clear the cart
    for item in cart_products:
        OrdersProducts.objects.create(order=order, product=item.product, quantity=item.quantity)
    
    # Clear the cart
    cart_products.delete()

    return redirect('order_summary', order_id=order.id)

def order_summary(request, order_id):
    # Get the order for the current user using UserOrders
    order = get_object_or_404(Order, id=order_id)
    
    # Check if the order is associated with the current user
    #user_order = get_object_or_404(UserOrders, user=request.user, order=order)
    
    # Retrieve the ordered products
    order_products = OrdersProducts.objects.filter(order=order)

    return render(request, 'order_summary.html', {
        'order': order,
        'order_products': order_products,
    })

@login_required  # Ensure that only logged-in users can access this page
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)  
    addresses = UserAddresses.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'user': request.user,
        'user_profile': user_profile,
        'addresses': addresses,
    })

