from django.shortcuts import render, redirect
from .models import Product, OrderDetail
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
import stripe, json
from django.urls import reverse
from .forms import ProductForm, UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import EmailAuthenticationForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


# Create your views here.
def index(request):
    products = Product.objects.filter().order_by("-created_at")
    return render(request, "myapp/index.html", {"products": products})


def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    tags = [tag.strip() for tag in product.tags.split(",")] if product.tags else []
    return render(
        request,
        "myapp/detail.html",
        {
            "product": product,
            "tags": tags,
            "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
        },
    )


@csrf_exempt
def create_checkout_session(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    try:
        request_data = json.loads(request.body)
        email = request_data.get("email")
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        product = get_object_or_404(Product, id=id)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        checkout_session = stripe.checkout.Session.create(
            customer_email=email,
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": product.title,
                        },
                        "unit_amount": int(product.discount_price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success"))
            + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("failed")),
        )

        OrderDetail.objects.create(
            customer_email=email,
            product=product,
            stripe_payment_intent=checkout_session.id,  # CHANGED
            amount=int(product.discount_price),
        )

        return JsonResponse({"sessionId": checkout_session.id})

    except Exception as e:
        print("Checkout session error:", e)
        return JsonResponse({"error": str(e)}, status=500)


def payment_success_view(request):
    session_id = request.GET.get("session_id")
    if session_id is None:
        return HttpResponseNotFound()
    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        return HttpResponseNotFound("Invalid session.")

    order = get_object_or_404(OrderDetail, stripe_payment_intent=session_id)

    order.has_paid = True

    product = Product.objects.get(id=order.product.id)
    product.total_sales_count += 1
    product.total_sales_amount += order.amount
    product.save()

    order.save()

    return render(request, "myapp/payment_success.html", {"order": order})


def payment_failed_view(request):
    return render(request, "myapp/payment_failed.html")

@login_required
def create_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            new_product = product_form.save(commit=False)
            new_product.seller = request.user
            new_product.save()
            return redirect("index")

    product_form = ProductForm()

    return render(request, "myapp/create_product.html", {"product_form": product_form})

@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.user != product.seller:
        return HttpResponseForbidden("Don't be oversmart this app has a strong backend. You are not allowed to edit this product.")
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect("index")
    else:
        product_form = ProductForm(instance=product)

    return render(request, "myapp/edit_product.html", {"product_form": product_form})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.user != product.seller:
        return HttpResponseForbidden("Don't be oversmart this app has a strong backend. You are not allowed to delete this product.")
    if request.method == "POST":
        product.delete()
        return redirect("index")

    return render(request, "myapp/delete_product.html", {"product": product})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # assuming email is used as username
            user.set_password(form.cleaned_data['password'])  
            user.save()
            return redirect('index')  
    else:
        form = UserRegistrationForm()

    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    form = EmailAuthenticationForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, "myapp/login.html", {"form": form})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")

@login_required
def my_purchases(request):
    orders = OrderDetail.objects.filter(customer_email__iexact=request.user.email, has_paid=True).select_related('product')
    return render(request, 'myapp/my_purchases.html', {'orders': orders})


@login_required
def dashboard(request):
    user = request.user
    products = Product.objects.filter(seller=user)
    total_sales = sum(p.total_sales_count for p in products)
    total_revenue = sum(p.total_sales_amount for p in products)
    context = {
        'products': products,
        'total_sales': total_sales,
        'total_revenue': total_revenue
    }
    return render(request, 'myapp/dashboard.html', context)

@login_required
def sales_analytics(request):
    user = request.user
    today = timezone.now().date()

    # Default range: last 30 days
    start_date = request.GET.get('start_date', (today - timedelta(days=29)).isoformat())
    end_date = request.GET.get('end_date', today.isoformat())

    # Fetch all orders (not grouped) for metrics
    all_orders = OrderDetail.objects.filter(
        product__seller=user,
        has_paid=True,
        created_on__date__gte=start_date,
        created_on__date__lte=end_date
    )

    # Total order count and revenue
    total_orders = all_orders.count()
    total_revenue = sum(order.amount for order in all_orders)

    # Grouped by day for chart
    grouped_orders = all_orders.values('created_on__date').annotate(daily_total=Sum('amount')).order_by('created_on__date')

    labels = [entry['created_on__date'].isoformat() for entry in grouped_orders]
    data = [float(entry['daily_total']) for entry in grouped_orders]

    return render(request, 'myapp/sales_analytics.html', {
        'labels': labels,
        'data': data,
        'start_date': start_date,
        'end_date': end_date,
        'total_revenue': total_revenue,
        'total_orders': total_orders
    })

@login_required
def order_list(request):
    user = request.user

    # Get all paid orders for this seller's products
    orders = OrderDetail.objects.filter(
        has_paid=True,
        product__seller=user
    ).select_related('product').order_by('-created_on')

    return render(request, 'myapp/order_list.html', {'orders': orders})