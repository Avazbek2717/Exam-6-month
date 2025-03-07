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



# class Review(serializers.ModelSerializer):


#     class Meta:
#         model = Review
#         fields = ()




class ReviewSerializer(serializers.ModelSerializer):
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



class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']