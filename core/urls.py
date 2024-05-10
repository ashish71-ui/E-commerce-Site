from django.urls import path
from core.views import index,category_list,category_product_list_view,vendor_list, vendor_product_list_view,product_detail_view,base
from django.conf import settings
from django.conf.urls.static import static
app_name ="core"

urlpatterns = [
    path('', base, name='base'),
    path('vendors/', vendor_list, name='vendor_list'),
    path('vendors/<vid>', vendor_product_list_view, name='vendor_product_list_view'),
     path('category/', category_list, name='category_list'),
     path('category/<cid>', category_product_list_view, name='category_product_list_view'),
      path('products/<pid>', product_detail_view, name='product_detail_view'),
      path('index',index, name='index'),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)