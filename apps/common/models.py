from django.db import models
from apps.users.models import User
from decimal import Decimal
from django.conf import settings


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
    poster = models.ImageField(upload_to='poster_image/')
    full_description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title

    def get_discount_price(self):
        return round(self.price * (Decimal('1') - Decimal(self.discount) / Decimal('100')), 2)



class Review(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews') 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    rating = models.PositiveIntegerField(default=5) 
    comment = models.TextField(null=True,blank=True)
 

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
    url  = models.URLField(blank=True,null=True)

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
    


from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Notification(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to="Notification/", null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def send_notification(self):
        """Bildirishnomani WebSocket orqali yuborish"""
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications_group",
            {
                "type": "send_notification",
                "title": self.title,
                "body": self.body,
                "image_url": self.image.url if self.image else None,
                "url": self.url
            }
        )

    def save(self, *args, **kwargs):
        """Saqlangandan keyin avtomatik ravishda bildirishnoma yuborish"""
        super().save(*args, **kwargs)
        self.send_notification()  
