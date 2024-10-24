from rest_framework import serializers
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount


class UserSerializer(serializers.ModelSerializer):
    
    profile_picture = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')
        
    def get_profile_picture(self, obj) -> str:
        
        try:
            social_account = SocialAccount.objects.get(user=obj)
            profile_picture_url = social_account.extra_data.get('picture', '')
            return profile_picture_url
        except SocialAccount.DoesNotExist:
            return ""
