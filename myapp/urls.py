from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>', views.detail, name='detail'),
    path('api/create-checkout-session/<int:id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/', views.payment_success_view, name='success'),
    path('payment-failed/', views.payment_failed_view, name='failed'),
    path('create-product/', views.create_product, name='create_product'),
    path('edit-product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-purchases/', views.my_purchases, name='my_purchases'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sales-analytics/', views.sales_analytics, name='sales_analytics'),
    path('orders/', views.order_list, name='order_list')
]
