from rest_framework import serializers
from .models import User, Profile
from posts.serializers import LikeSerializer, PostSerializer


########################################################################
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.pk', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'user_id', 'bio', 'image']

    # ----------------------------------------------------------------------
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('nested'):  # Check if the context specifies that this is a nested serializer
            data.pop('username')  # If it is, remove the 'user' field from the serialized data
            data.pop('user_id')
        return data


########################################################################
class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'id', 'email', 'role', 'profile', 'posts', 'likes']

    # ----------------------------------------------------------------------
    def get_profile(self, obj):
        profile = ProfileSerializer(obj.profile, context={'nested': True})
        return profile.data

    # ----------------------------------------------------------------------
    def get_posts(self, obj):
        profile = PostSerializer(obj.posts, context={'nested': True}, many=True)
        return profile.data

    # ----------------------------------------------------------------------
    def get_likes(self, obj):
        profile = LikeSerializer(obj.likes, context={'nested': True}, many=True)
        return profile.data

    # ----------------------------------------------------------------------
    def create(self, validated_data):
        profile_data = self.initial_data.pop('profile')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    # ----------------------------------------------------------------------
    def update(self, instance, validated_data):
        profile_data = self.initial_data.pop('profile', None)
        instance = super().update(instance, validated_data)

        if profile_data is not None:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance

