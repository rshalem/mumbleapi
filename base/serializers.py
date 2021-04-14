from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField(read_only=True)
    interests = serializers.SerializerMethodField(read_only=True)
    skills = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

    def get_profile_pic(self, obj):
        try:
            pic = 'static' + obj.profile_pic.url
        except:
            pic = None
        return pic

    def get_interests(self, obj):
        return ['Python', 'C#', 'D3 Charts', 'Flutter']

    def get_skills(self, obj):
        return ['Python', 'C#', 'D3 Charts', 'Flutter']


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = '__all__'

    def get_profile(self, obj):
        profile = obj.userprofile
        serializer = UserProfileSerializer(profile, many=False)
        return serializer.data


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)



class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    origional_mumble = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data


    def get_origional_mumble(self, obj):
        origional = obj.remumble
        if origional != None:
            serializer = PostSerializer(origional, many=False)
            return serializer.data
        else:
            return None

