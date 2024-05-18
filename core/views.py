from django.shortcuts import render, HttpResponse
from core.models import CartOrder,Category,Vendor,Product,ProductImages,ProductReview,CartOrderItems,WishList,Address
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string



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
    context = {'cart': cart}
    return render(request, 'core/cart.html', context)

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