from rest_framework import serializers
from .models import Post, Comment, Like, Tag


########################################################################
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'id']


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.pk', read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'author_id', 'title', 'content',
                  'published_at', 'category', 'tags']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('nested'):
            data.pop('author_username')
            data.pop('author_id')
        return data


########################################################################
class CommentSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_id = serializers.IntegerField(source='post.id', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user_username', 'user_id', 'post_title', 'post_id', 'text']


########################################################################
class LikeSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user_username', 'user_id', 'post', 'comment']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('nested'):  # Check if the context specifies that this is a nested serializer
            data.pop('user_username')  # If it is, remove the 'user' field from the serialized data
            data.pop('user_id')
        return data
