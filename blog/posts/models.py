from django.db import models


########################################################################
class Post(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=200)
    tags = models.CharField(max_length=500)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


########################################################################
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


########################################################################
class Comment(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField()


########################################################################
class Like(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True)
