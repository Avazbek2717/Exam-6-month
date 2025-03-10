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
        fields = ('email', 'is_active')


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ("id", "name", "poster")