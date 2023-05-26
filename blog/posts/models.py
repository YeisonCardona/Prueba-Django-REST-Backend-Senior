from django.db import models


########################################################################
class Post(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=200)
    tags = models.ManyToManyField('Tag')


########################################################################
class Tag(models.Model):
    name = models.CharField(max_length=100)


########################################################################
class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()


########################################################################
class Like(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, related_name='likes')
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='comments')
