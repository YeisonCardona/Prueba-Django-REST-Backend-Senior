import django_filters
from .models import Post, Comment, Like


########################################################################
class PostFilter(django_filters.FilterSet):
    author_username = django_filters.CharFilter(field_name='author__username')
    title = django_filters.CharFilter(lookup_expr='icontains')
    content = django_filters.CharFilter(lookup_expr='icontains')
    published_after = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = django_filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')
    category = django_filters.CharFilter()
    tags = django_filters.CharFilter(field_name='tags__name')

    class Meta:
        model = Post
        fields = ['author_username', 'title', 'content', 'published_after', 'published_before', 'category', 'tags']


########################################################################
class CommentFilter(django_filters.FilterSet):
    user_username = django_filters.CharFilter(field_name='user__username')
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    text = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Comment
        fields = ['user_username', 'post_title', 'text']


########################################################################
class LikeFilter(django_filters.FilterSet):
    user_username = django_filters.CharFilter(field_name='user__username')
    post_title = django_filters.CharFilter(field_name='post__title', lookup_expr='icontains')
    comment_text = django_filters.CharFilter(field_name='comment__text', lookup_expr='icontains')

    class Meta:
        model = Like
        fields = ['user_username', 'post_title', 'comment_text']
