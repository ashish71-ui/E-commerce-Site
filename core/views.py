from django.shortcuts import render, HttpResponse
from core.models import CartOrder,Category,Vendor,Product,ProductImages,ProductReview,CartOrderItems,WishList,Address
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.conf import settings
import uuid
import hmac
import hashlib
from django.views.decorators.csrf import csrf_exempt
from .models import CartOrder, CartOrderItems
from .forms import UpdateQuantityForm, DeleteItemForm
import base64

from django.views.decorators.http import require_POST

def base(request):
    products = Product.objects.all().order_by("-id")
    categories = Category.objects.all()
    
    # products = Product.objects.filter(featured = True).order_by("-id")
    context = {
        "products":products,
         "categories":categories
    }
    return render(request,'core/base.html',context)

def index(request):
    products = Product.objects.all().order_by("-id")
    # products = Product.objects.filter(featured = True).order_by("-id")
    context = {
        "products":products
    }
    return render(request,'core/index.html',context)

def category_list(request):
    categories = Category.objects.all()
    context = {
        "categories":categories
    }
    return render(request,'core/category_list.html',context)

def category_product_list_view(request,cid):
    category = Category.objects.get(cid=cid)
    # products = Product.objects.filter(product_status ="published",category = category)
    products = Product.objects.filter(category = category)
    context = {
        "category":category,
        "products":products
    }
    return render(request,'core/category_product_list_view.html',context)

def vendor_list(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors":vendors
    }
    return render(request,'core/vendor_list.html',context)
def vendor_product_list_view(request,vid):
    vendor = Vendor.objects.get(vid=vid)
    # products = Product.objects.filter(product_status ="published",category = category)
    products = Product.objects.filter(vendor = vendor)
    context = {
        "vendors":vendor,
         "products":products
    }
    return render(request,'core/vendor_product_list_view.html',context)

def product_detail_view(request,pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_image.all()
    r_product = Product.objects.filter(category = product.category).exclude(pid=pid)
    context = {
        
         "product":product,
         "p_image":p_image,
         "r_product":r_product
    }
    return render(request,'core/product_detail_view.html',context)

def search(request):
    query = request.GET.get("query")
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    context = {
        "products":products,
        "query":query
    }
    return render(request,'core/search.html',context)
@login_required
def add_to_cart(request, pid):
    product = get_object_or_404(Product, pid=pid)
    
    # Get or create a cart for the user
    cart, created = CartOrder.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item = CartOrderItems.objects.filter(order=cart, product=product).first()
    
    # If the item is already in the cart, update quantity
    if cart_item:
        cart_item.qty += 1
        cart_item.save()
    else:
        # If the item is not in the cart, create a new cart item
        cart_item = CartOrderItems.objects.create(order=cart, product=product, qty=1)
    
    return redirect('core:cart_view')   
@login_required
def cart_view(request):
    cart = CartOrder.objects.filter(user=request.user).first()
    total_price = 0

    if cart:
        for item in cart.cartorderitems_set.all():
            total_price += item.product.price * item.qty

    context = {'cart': cart, 'total_price': total_price}
    return render(request, 'core/cart.html', context)
@login_required
@require_POST
def update_cart_item(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    item = get_object_or_404(CartOrderItems, id=item_id, order__user=request.user)

    if action == 'increase':
        item.qty += 1
    elif action == 'decrease' and item.qty > 1:
        item.qty -= 1
    item.save()

    return JsonResponse({'qty': item.qty})
def final_payment(request):
    cart = CartOrder.objects.filter(user=request.user).first()
    total_price = 0
    delivery_charge = 100
    

    if cart:
        for item in cart.cartorderitems_set.all():
            total_price += item.product.price * item.qty
    tax = 0
    final_price = total_price + delivery_charge + tax
    context = {'cart': cart, 'total_price': total_price,"delivery_charge":delivery_charge,"final_price":final_price,'tax':tax}
    return render(request, 'core/cart.html', context)

@login_required
@require_POST
def delete_cart_item(request):
    item_id = request.POST.get('item_id')
    item = get_object_or_404(CartOrderItems, id=item_id, order__user=request.user)
    item.delete()
    return JsonResponse({'success': True})
def product_list(request):
    vendor_ids = request.GET.get('vendors', '').split(',')
    category_ids = request.GET.get('categories', '').split(',')

    products = Product.objects.all()

    if vendor_ids != ['']:
        products = products.filter(vendor__vid__in=vendor_ids)
    
    if category_ids != ['']:
        products = products.filter(category__cid__in=category_ids)

    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        html = render_to_string('product_list_partial.html', {'products': products})
        return JsonResponse({'html': html})

    context = {
        'products': products,
        'vendors': Vendor.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'core/product_list_partial.html', context)



# payment


def generate_signature(total_amount, transaction_uuid, product_code, secret_key):
    concatenated_data = f'total_amount={total_amount}&transaction_uuid={transaction_uuid}&product_code={product_code}'
    signature = hmac.new(secret_key.encode('utf-8'), concatenated_data.encode('utf-8'), hashlib.sha256).digest()
    base64_signature = base64.b64encode(signature).decode('utf-8')
    return base64_signature

def initiate_payment(request):
    # Generate unique transaction ID
    transaction_id = uuid.uuid4()

    # Prepare payment data
    payment_data = {
        'amount': 200,
        'tax_amount': 10,
        'total_amount': 110,
        'transaction_uuid': transaction_id,
        'product_code': 'EPAYTEST',
        'product_service_charge': 0,
        'product_delivery_charge': 0,
        'success_url': request.build_absolute_uri('/payment/success/'),
        'failure_url': request.build_absolute_uri('/payment/failure/'),
        'signed_field_names': 'total_amount,transaction_uuid,product_code',
    }

    # Generate signature
    secret_key = "8gBm/:&EnhH.1/q"
    
    signature = generate_signature(payment_data['total_amount'], payment_data['transaction_uuid'], payment_data['product_code'], secret_key)

    context = {
        'payment_data': payment_data,
        'signature': signature,
        'esewa_payment_url': 'https://rc-epay.esewa.com.np/api/epay/main/v2/form',
    }

    return render(request, 'core/initiate_payment.html', context)


@csrf_exempt
def payment_success(request):
    # Handle successful payment here
    return render(request, 'payment/success.html')


@csrf_exempt
def payment_failure(request):
    # Handle failed payment here
    return render(request, 'payment/failure.html')