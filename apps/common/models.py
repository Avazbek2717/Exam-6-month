from django.db import models
from apps.users.models import User


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract=True


class Category(BaseModel):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
  
    
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to="products/")


class Range(BaseModel):
    pass
    

class Product(BaseModel):

    class SelectSize(models.TextChoices):
        SMALL = 's', 'S'
        MEDIUM = 'm', 'M'
        LARGE = 'l', 'L'
        EXTRA_LARGE = 'xl', 'XL'

    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    short_description = models.TextField()
    size = models.CharField(max_length=5, choices=SelectSize.choices)
    discount = models.IntegerField(null=True, blank=True)
    category = models.ManyToManyField('Category')
    tag = models.ManyToManyField('Tag')
    image = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='products_image')
    full_description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_discount_price(self):
    
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price


class Review(BaseModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews') 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField(default=5) 
    comment = models.TextField()
 

    def __str__(self):
        return f"{self.user} - {self.product} ({self.rating})"
    

class Order(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.full_name}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
    

class ContactUs(BaseModel):
    full_name = models.CharField(BaseModel)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.full_name


class Founder(BaseModel):
    name  = models.CharField(max_length=200)
    image = models.ImageField(upload_to='founder/')
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    

class Testimonial(BaseModel):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    feedback = models.TextField()

    def __str__(self):
        return self.name
    

class Banner(BaseModel):
    name = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='poster/')

    def __str__(self):
        return self.name
    

class Subscriber(models.Model):
    email = models.EmailField(unique=True) 
    subscribed_at = models.DateTimeField(auto_now_add=True)  
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return self.email
    

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title