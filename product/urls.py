from django.urls import path

from . import views

urlpatterns =[
     path('' , views.index, name='index'),
      path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
     path('reject_user/<int:user_id>/', views.reject_user, name='reject_user'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/', views.products, name='product'),

    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('my/dashboard/', views.customer_dashboard, name='customer_dashboard'),    
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    path('approve_order_service/<int:order_id>/', views.approve_order_service, name='approve_order_service'),
    path('decline_order_service/<int:order_id>/', views.decline_order_service, name='decline_order_service'),


  path('checkout/', views.checkout, name='checkout'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout-cart/', views.checkout_cart, name='checkout_cart'),
        path('add-service-to-order/', views.add_service_to_order, name='add_service_to_order'),

 path('process-checkout/', views.process_checkout, name='process_checkout'),

  path('dashboard/', views.dashboard, name='dashboard'),
    path('manage-services/', views.manage_order_services, name='manage_services'),
    path('add-product/', views.add_product, name='add_product'),
    path('add-service/', views.add_service, name='add_service'),
    path('approve-service/', views.approve_service, name='approve_service'),
    path('delete-service/', views.delete_service, name='delete_service'),
    
    
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
   


   


]

