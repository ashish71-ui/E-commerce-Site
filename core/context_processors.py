

from .models import Vendor, Category

def vendor_and_category(request):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    return {
        'vendors': vendors,
        'categories': categories,
    }
