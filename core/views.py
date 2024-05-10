from django.shortcuts import render, HttpResponse
from core.models import CartOrder,Category,Vendor,Product,ProductImages,ProductReview,CartOrderItems,WishList,Address


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
    context = {
        
         "product":product,
         "p_image":p_image
    }
    return render(request,'core/product_detail_view.html',context)