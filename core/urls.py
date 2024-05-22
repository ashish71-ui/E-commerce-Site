from django.urls import path
from core.views import index,category_list,category_product_list_view,vendor_list, vendor_product_list_view,product_detail_view,base,search,add_to_cart,cart_view,product_list
from django.conf import settings
from django.conf.urls.static import static
from core import views
app_name ="core"

urlpatterns = [
    path('', base, name='base'),
    path('vendors/', vendor_list, name='vendor_list'),
    path('vendors/<vid>', vendor_product_list_view, name='vendor_product_list_view'),
    path('category/', category_list, name='category_list'),
    path('category/<cid>', category_product_list_view, name='category_product_list_view'),
    path('products/<pid>', product_detail_view, name='product_detail_view'),
    path('index',index, name='index'),
    path('search',search, name='search'),
    path('add_to_cart/<pid>/', add_to_cart, name='add_to_cart'),
    path('cart_view/', cart_view, name='cart_view'),
     path('products/', product_list, name='product_list'),
     path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),
      path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('delete-cart-item/', views.delete_cart_item, name='delete_cart_item'),
    path('final_payment/', views.final_payment, name='final_payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)