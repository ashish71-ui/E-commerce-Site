from django.db import models
from userauths.models import User
from django.db import models
from django.utils.html import mark_safe


STATUS_CHOICE = (
    ("process","Processing"),
    ("shipped","Shipped"),
    ("delivered","Delivered")
)

STATUS = (
    ("draft","Draft"),
    ("disabled","Disabled"),
    ("rejected","Rejected"),
    ("in_review","In Review"),
    ("published","Published")
)
RATING = (
    (1,"✨"),
    (2,"✨✨"),
    (3,"✨✨✨"),
    (4,"✨✨✨✨"),
    (5,"✨✨✨✨✨")
)


def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)
class Category(models.Model):
    cid = models.UUIDField(unique=True)
    title = models.CharField(max_length=100,default="Category")
    image = models.ImageField(upload_to="category/images",default="category.jpg")
    class Meta:
        verbose_name_plural = "Categories"
    def category_image(self):
        return mark_safe('< img src ="%s" width = "50" height = "50"/ >'% (self.image.url))
    def __str__(self) :
        return self.title
class Tags(models.Model):
    pass    
    
class Vendor(models.Model):
    vid = models.UUIDField(unique=True)
    title = models.CharField(max_length=100,default="weger")
    image = models.ImageField(upload_to='vendor/images',default="vendor.jpg")
    description = models.TextField(null=True,blank=True,default="this is vendor")
    address = models.CharField(max_length=100,default='kalanki')
    contact = models.CharField(max_length=100,default='123')
    chat_resp_time = models.CharField(max_length=100,default='123')
    shipping_on_time = models.CharField(max_length=100,default='123')
    authentic_rating = models.CharField(max_length=100,default='123')
    days_return = models.CharField(max_length=100,default='123')
    warranty_period = models.CharField(max_length=100,default='123')
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
    def vendor_image(self):
        return mark_safe('< img src ="%s" width = "50" height = "50"/ >'% (self.image.url))
    def __str__(self) :
        return self.title
    
    
class Product(models.Model):
    pid = models.UUIDField(unique=True)
    title = models.CharField(max_length=100,default="products")
    image = models.ImageField(upload_to='product/images',default="product.jpg")
    description = models.TextField(null=True,blank=True,default="this is description")
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL,null=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL,null=True)
    price = models.DecimalField(max_digits=99999999,decimal_places=3,default="199")
    old_price = models.DecimalField(max_digits=99999999,decimal_places=3,default="299")
    specificaions = models.TextField(null=True,blank=True,default="this is specifications")
    product_status = models.CharField(choices=STATUS,max_length=10,default="in_review")
    
    status = models.BooleanField(default=True)
    in_Stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = models.UUIDField(unique=True)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True,blank=True)


    class Meta:
            verbose_name_plural = "Products"
    def product_image(self):
            return mark_safe('< img src ="%s" width = "50" height = "50"/ >'% (self.image.url))
    def __str__(self) :
            return self.title
    def get_percentage(self):
        new_price = (self.price/self.old_price)*100
        return new_price
    
    
    
    
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images/images",default="product.jpg")
    product = models.ForeignKey(Product,related_name='p_image', on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            verbose_name_plural = "Product Images"
    
    
    
    

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999999,decimal_places=3,default="199")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS,max_length=300000000,default="processing")
    
    class Meta:
          verbose_name_plural = "Cart Order"
          
    
    
class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999,decimal_places=3,default="199")
    total = models.DecimalField(max_digits=99999999,decimal_places=3,default="199")
    
    class Meta:
          verbose_name_plural = "Cart Order Items"
          
    def order_img(self):
         return mark_safe('< img src ="/media/%s" width = "50" height = "50"/ >'% (self.image))
     
     
     
     
class ProductReview(models.Model):
   
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
          
    def __str__(self) :
        return self.product.title   
    def get_rating(self) :
        return self.rating
    
    
class WishList(models.Model):
   
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlists"
          
    def __str__(self) :
        return self.product.title   
    
    
    
class Address(models.Model):
    
  user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
  address = models.CharField(max_length=100,null=True)
  status = models.BooleanField(default=True)
  class Meta:
        verbose_name_plural = "Addresses"