from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, PostRate, UserActivity


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], None, validated_data['password'])
        return user
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PostSerializer(serializers.HyperlinkedModelSerializer):
    count_likes = serializers.IntegerField(source='get_likes_count', required=False)

    class Meta:
        model = Post
        fields = ['id', 'url', 'text', 'pub_date', 'posted_by', 'count_likes']


class PostRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostRate
        fields = '__all__'
        read_only_fields = ['rated_by', 'rated_post', 'rate_date', 'url']


class UserActivitySerializer(serializers.HyperlinkedModelSerializer):
    last_login = serializers.DateTimeField(source='get_last_login')
    
    class Meta:
        model = UserActivity
        fields = '__all__'
