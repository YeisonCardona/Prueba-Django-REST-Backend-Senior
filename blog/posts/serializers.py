from rest_framework import serializers
from .models import Post, Comment, Like, Tag
from users.models import User


########################################################################
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'id']


########################################################################
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.pk', read_only=True)
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Post
        fields = ['id', 'author_username', 'author_id', 'title', 'content',
                  'published_at', 'category', 'tags']

    # ----------------------------------------------------------------------
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('nested'):
            data.pop('author_username')
            data.pop('author_id')
        return data

    # ----------------------------------------------------------------------
    def create(self, validated_data):
        tags_data = self.initial_data.pop('tags')
        author_id = self.initial_data.pop('author_id')
        author = User.objects.get(pk=author_id)
        post = Post.objects.create(author=author, **validated_data)

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return post

    # ----------------------------------------------------------------------
    def update(self, instance, validated_data):
        tags_data = self.initial_data.pop('tags')
        instance = super().update(instance, validated_data)

        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance


########################################################################
class CommentSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id')
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_id = serializers.IntegerField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'user_username', 'user_id', 'post_title', 'post_id', 'text']

    # ----------------------------------------------------------------------
    def create(self, validated_data):
        user_id = validated_data.pop('user')
        user = User.objects.get(pk=user_id['id'])
        post_id = validated_data.pop('post')
        post = Post.objects.get(pk=post_id['id'])
        comment = Comment.objects.create(user=user, post=post, **validated_data)
        return comment

    # ----------------------------------------------------------------------
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance


########################################################################
class LikeSerializer(serializers.ModelSerializer):

    user_username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user_username', 'user_id', 'post', 'comment']

    # ----------------------------------------------------------------------
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('nested'):
            data.pop('user_username')
            data.pop('user_id')
        return data

    # ----------------------------------------------------------------------
    def create(self, validated_data):
        user_id = self.initial_data.copy().pop('user_id')
        user = User.objects.get(pk=user_id)
        comment = Like.objects.create(user=user, **validated_data)
        return comment
