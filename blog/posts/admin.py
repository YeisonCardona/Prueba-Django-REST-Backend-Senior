from django.contrib import admin
from .models import Post, Comment, Like, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_at', 'category', 'display_tags')
    search_fields = ['title', 'author__username', 'category']
    list_filter = ('category', 'author')

    def display_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    display_tags.short_description = 'Tags'


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text')
    search_fields = ['user__username', 'post__title', 'text']


admin.site.register(Comment, CommentAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment')
    search_fields = ['user__username', 'post__title', 'comment__text']


admin.site.register(Like, LikeAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(Tag, TagAdmin)
