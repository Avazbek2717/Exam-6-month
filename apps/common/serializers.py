from rest_framework import serializers
from .models import *



from rest_framework import serializers
from .models import News

class NewsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['title', 'content']


class SendEmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscriber
        fields = ['email']


class BannerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Banner
        fields = ['name', 'poster']


class ReviewSerializer1(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "created_at"]

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    size_display = serializers.CharField(source="get_size_display", read_only=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()  

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'discount_price', 'short_description', 'size_display',
            'discount', 'poster', 'full_description', 'rating', 'category', 'tag', 'reviews'
        ]

    def get_category(self, obj):
        return [category.name for category in obj.category.all()]

    def get_tag(self, obj):
        return [tag.name for tag in obj.tag.all()]

    def get_discount_price(self, obj):
        return obj.get_discount_price()

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return ReviewSerializer(reviews, many=True).data

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return 0 
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(), 1) 



from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','product', 'rating', 'comment', 'user']  
    
    def validate_rating(self,value):
        if 5 >= value:
            raise serializers.ValidationError('Siz 5 dan baland baxo qoya olmaysiz!')
        return value

    def validate_comment(self,value):
        if len(value)>=10:
            raise serializers.ValidationError('Commentni koproq yozing!')

class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        exclude = ('created_at','updated_at')

    def validate_email(self,value):

        if '@' not in value:
            raise serializers.ValidationError("Email notog'ri kiritilyapti")
        return value
    
    def validate_message(self,value):
        print(len(value))
        if len(value)<10:
            raise serializers.ValidationError("So'z o'ntadan kam bo'lmasligi mumkin")
        return value
    
class NewArrivalsSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Product
        fields = ('id','title','poster','price')


class TestimonalSerializer(serializers.ModelSerializer):


    class Meta:
        model = Testimonial
        exclude = ['created_at',"updated_at"]




class OrderItemSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)  # Faqat o‘qish uchun

    class Meta:
        model = OrderItem
        fields = '__all__'

    def validate_quantity(self, value):
        """ Mahsulot soni 1 dan kam bo‘lmasligi kerak """
        if value < 1:
            raise serializers.ValidationError("Mahsulot soni kamida 1 bo‘lishi kerak.")
        return value

    def validate(self, data):
        """ Mahsulot omborda yetarli ekanligini tekshirish va price ni productdan olish """
        product = data.get('product')
        quantity = data.get('quantity')

        if product and quantity:
            if product.stock < quantity:
                raise serializers.ValidationError(f"{product.title} mahsuloti uchun yetarli ombor zaxirasi mavjud emas.")
            # Mahsulot narxini avtomatik tarzda olish
            data['price'] = product.price
        
        return data
    def create(self, validated_data):
        product = validated_data.get('product')
        validated_data['price'] = product.price  # Narxni avtomatik olish
        return super().create(validated_data)
        


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = "__all__"

    def validate_phone(self, value):
        """ Telefon raqami to'g'ri formatda ekanligini tekshirish """
        if not value.isdigit() or len(value) < 9:
            raise serializers.ValidationError("Telefon raqami noto‘g‘ri kiritilgan.")
        return value

    def validate_email(self, value):
        """ Email to'g'ri formatda ekanligini tekshirish """
        if "@" not in value or "." not in value:
            raise serializers.ValidationError("Yaroqsiz email manzil.")
        return value

    def get_total_price(self, obj):
        """ Order ichidagi barcha OrderItem narxlarini qo‘shish """
        return sum(item.price for item in obj.items.all())


from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
