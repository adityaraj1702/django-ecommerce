from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),#homepage url
    path('test', views.test, name='test'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('product/<int:pk>', views.product, name='product'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('register/', views.register, name='register'),
    path('seller/', views.seller_page, name='seller_page'),
    path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('profile/', views.profile, name='profile'),
]