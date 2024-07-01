from django.shortcuts import render
from .models import Product, Cart,  User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User as user
from django.db import connection
from .models import Product, Cart,  User, Services
from django.contrib.auth.decorators import login_required


from functools import wraps
from django.shortcuts import redirect




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Role, Order_product , Order_Services


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        approved = 1 
        if role == 'Farmer':
            approved = 0
        else :
            approved = 1

        # Create User
        user = User.objects.create_user(username=username, password=password)
        
        # Create Role
        Role.objects.create(user=user, role=role, approved=approved)
        
        if role == 'admin':
            messages.info(request, 'Admin account created. Waiting for approval.')
        elif role == 'farmer':
            messages.info(request, 'Farmer account created. Waiting for approval.')
        elif role == 'customer':
              auth_login(request, user)
              return redirect('customer_dashboard')

        else:
            messages.success(request, 'Registration successful. You can now log in.')
        
        
        return redirect('login')
    users = request.user
    users_d = Role.objects.get(user=users)

    return render(request, 'product/signup.html' , {'users': users_d})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import User, Role

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                messages.success(request, 'Login successful!')

                # Redirect based on user role
                if user.is_superuser:
                    return redirect('admin_dashboard')
                else:
                    try:
                        user_role = Role.objects.get(user=user)
                        if user_role.role == 'farmer':
                            return redirect('customer_dashboard')
                        elif user_role.role == 'customer':
                            return redirect('customer_dashboard')
                        else:
                            messages.error(request, 'Unknown user role.')
                            return redirect('logout')  # Log out if role is not recognized
                    except Role.DoesNotExist:
                        messages.error(request, 'User role not defined.')
                        return redirect('logout')

            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
   


    return render(request, 'product/login.html' )



def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            # Redirect to login or show an error page
            return redirect('login')  # Adjust 'login' to your actual login URL
        return view_func(request, *args, **kwargs)
    return wrapper


def index(request):   
    users = request.user
    users_d = Role.objects.get(user=users)
 
    return render(request, 'product/index.html', {'users' : users_d})

def products(request):   
    users = request.user
    users_d = Role.objects.get(user=users)
    products = Product.objects.all()

 
    return render(request, 'product/product.html', {'products': products,'users' : users_d})


def about(request):
    users = request.user
    users_d = Role.objects.get(user=users)
 
    return render(request, 'product/about.html' , {'users' : users_d})

def services(request):
        users = request.user
        users_d = Role.objects.get(user=users)
    
    
        products = Services.objects.all()
        return render(request, 'product/services.html', {'services': products, 'users' : users_d})
   

def product_detail(request, product_id):
        users = request.user
        users_d = Role.objects.get(user=users)
    
        product = Product.objects.get(id=product_id)
        return render(request, 'product/product_detail.html', {'product': product , 'users' : users_d})
  
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        user_id = request.session['user_id']
        product = Product.objects.get(id=product_id)
        Cart.objects.create(user_id=user_id, product=product, quantity=quantity)
        messages.success(request, 'Item added to cart')
    return redirect('services')

def cart(request):
    if request.session.get('username'):
        user_id = request.session['user_id']
        cart_items = Cart.objects.filter(user_id=user_id).select_related('product')
        return render(request, 'cart.html', {'cart_items': cart_items})
    else:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')

def checkout(request):
    '''
    if request.session.get('username'):
        user_id = request.session['user_id']
        cart_items = Cart.objects.filter(user_id=user_id).select_related('product')
        total = sum(item.product.price * item.quantity for item in cart_items)
        Order.objects.create(user_id=user_id, total=total)
        Cart.objects.filter(user_id=user_id).delete()
        messages.success(request, 'Checkout successful!')
        return redirect('services')
    else:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')
    '''
    pass

def profile(request):
    if request.session.get('username'):
        user = {
            'username': request.session['username'],
            'email': 'user@example.com',
            'profile_picture': request.session['profile_picture'],
        }
        return render(request, 'product/profile.html', {'user': user})
    else:
        messages.error(request, 'Please log in to access this page.')
        return redirect('login')



from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, User

@login_required
@admin_required
def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User rejected successfully.')
    return redirect('manage_users')

@login_required
@admin_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = float(request.POST['price'])
        image = request.POST['image']
        Product.objects.create(name=name, description=description, price=price, image=image)
        messages.success(request, 'Product added successfully.')
        return redirect('services')
    return render(request, 'product/product_form.html')

@login_required
@admin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = float(request.POST['price'])
        product.image = request.POST['image']
        product.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('services')
    return render(request, 'product/product_form.html', {'product': product})

@login_required
@admin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('services')
  


@login_required
@admin_required
def admin_dashboard(request):
    users = request.user
    users_d = Role.objects.get(user=users)
 
    return render(request, 'product/admin_dashboard.html')

def customer_dashboard(request):
    users = request.user
    users_d = Role.objects.get(user=users)
    farmers_order = Order_Services.objects.filter(farmer=users)
    product_order = Order_product.objects.filter(customer=users)


    


    return render(request, 'product/user_dashboard.html', {'users': users_d, 'farmers_order': farmers_order, 'product_order': product_order})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Cart

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user_id=request.user, product=product)
        else:
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_id, product=product)

        if created:
            cart.quantity = quantity  # Set the initial quantity
        else:
            cart.quantity += quantity  # Increment the existing quantity

        cart.save()

        messages.success(request, 'Item added to cart!')

        return redirect('product')  # Adjust to your product listing URL name

    return JsonResponse({'message': 'Invalid request'}, status=400)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order_product
from django.utils import timezone

@login_required
def process_checkout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user_id=request.user)
        else:
            session_id = request.session.session_key
            cart_items = Cart.objects.filter(session_id=session_id)

        total = sum(item.product.price * item.quantity for item in cart_items)

        for item in cart_items:
            order = Order_product(
                customer=request.user,
                product=item.product,
                quantity=item.quantity,
                total=item.product.price * item.quantity,
                created_at=timezone.now()
            )
            order.save()

        cart_items.delete()
        messages.success(request, 'Checkout successful! Your order has been placed.')

        return redirect('customer_dashboard')  # Adjust to your product listing URL name

    return JsonResponse({'message': 'Invalid request'}, status=400)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order_product

def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user_id=request.user)
    else:
        session_id = request.session.session_key
        cart_items = Cart.objects.filter(session_id=session_id)
        
    users = request.user
    users_d = Role.objects.get(user=users)  
    
    return render(request, 'product/checkout.html', { 'users': users_d,'cart_items': cart_items})

def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = request.POST.get('quantity')
        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'message': 'Item updated'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)

def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.delete()
        return JsonResponse({'message': 'Item removed'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)

def checkout_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(user_id=request.user)
        else:
            return JsonResponse({'message': 'User not authenticated'}, status=400)

        for item in cart_items:
            order_product = Order_product(
                customer=request.user,
                product=item.product,
                total=item.product.price * item.quantity,
                quantity=item.quantity
            )
            order_product.save()
        cart_items.delete()
        return JsonResponse({'message': 'Checkout successful'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Services, Order_Services

@login_required
def add_service_to_order(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Services, id=service_id)

        order_service = Order_Services.objects.create(
            farmer=request.user,
            services=service,
            name=service.name,
            description=service.description,
            Approval=service.Approval
        )

        return JsonResponse({'message': 'Service added to order!'}, status=200)

    return JsonResponse({'message': 'Invalid request'}, status=400)



import logging

logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    users = request.user
    
    # Check if the user has an associated role
    try:
        users_d = Role.objects.get(user=users)
    except Role.DoesNotExist:
        users_d = None  # or handle this case appropriately
        logger.error(f'Role does not exist for user: {users.username}')
    
    # Get the counts of farmers and customers
    farmers_count = Role.objects.filter(role='farmer').count()
    customers_count = Role.objects.filter(role='customer').count()
    
    # Log the counts for debugging
    logger.info(f'Farmers count: {farmers_count}')
    logger.info(f'Customers count: {customers_count}')
    
    # Get the recent orders
    recent_orders = Order_product.objects.all().order_by('-created_at')[:10]
    
    context = {
        'farmers_count': farmers_count,
        'customers_count': customers_count,
        'recent_orders': recent_orders,
        'users': users_d,
        
    }
    
    return render(request, 'product/admin_dashboard.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order_Services


@login_required
def approve_order_service(request, order_id):
    order = get_object_or_404(Order_Services, id=order_id)
    order.Approval = True
    order.save()
    return redirect('manage_services')

@login_required
def decline_order_service(request, order_id):
    order = get_object_or_404(Order_Services, id=order_id)
    order.Approval = False
    order.save()
    return redirect('manage_services')


# views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests

# Replace with your Paystack API keys
PAYSTACK_SECRET_KEY = 'pk_live_504e9f8c8aebfa975ff87ba801235867f91f39f9'

# Endpoint to initiate payment
def initiate_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Example: Use Paystack's initialize transaction endpoint
        response = initialize_transaction(amount, email, phone_number)

        return JsonResponse(response)

    return render(request, 'product/initiate_payment.html')

# Function to initialize transaction with Paystack
def initialize_transaction(amount, email, phone_number):
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        'Authorization': f'Bearer {PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'amount': amount,
        'email': email,
        'phone': phone_number,
        'currency': 'KES',  # Currency code for Kenya Shilling
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Endpoint to handle Paystack webhook/callback
def payment_callback(request):
    if request.method == 'POST':
        # Handle Paystack's webhook/callback
        # Verify and process payment status
        # Example: Check if payment was successful
        event_data = request.body.decode('utf-8')
        # Process event_data and update your application accordingly
        return JsonResponse({'message': 'Payment received'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def manage_order_services(request):
    orders = Order_Services.objects.all()
    users = request.user
    users_d = Role.objects.get(user=users)
    
    return render(request, 'product/manage_services.html', {'orders': orders, 'users' : users_d})

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Product

@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        Product.objects.create(name=name, price=price, description=description)

        return JsonResponse({'message': 'Product added successfully!'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)


@login_required
def add_service(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        Services.objects.create(name=name, description=description)

        return JsonResponse({'message': 'Service added successfully!'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def approve_service(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Services, id=service_id)
        service.Approval = True
        service.save()
        return JsonResponse({'message': 'Service approved successfully!'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)

@login_required
def delete_service(request):
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        service = get_object_or_404(Services, id=service_id)
        service.delete()
        return JsonResponse({'message': 'Service deleted successfully!'}, status=200)
    return JsonResponse({'message': 'Invalid request'}, status=400)



