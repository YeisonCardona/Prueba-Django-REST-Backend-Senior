from rest_framework import viewsets
from .models import Post, Comment, Like, Tag
from .serializers import PostSerializer, CommentSerializer, LikeSerializer, TagSerializer
from users.permissions import IsAdmin, IsEditor, IsBlogger
from .filters import PostFilter, CommentFilter, LikeFilter


########################################################################
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdmin | IsEditor | IsBlogger]
    filterset_class = PostFilter


########################################################################
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdmin | IsEditor | IsBlogger]
    filterset_class = CommentFilter


########################################################################
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAdmin | IsEditor | IsBlogger]
    filterset_class = LikeFilter


########################################################################
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdmin | IsEditor | IsBlogger]
