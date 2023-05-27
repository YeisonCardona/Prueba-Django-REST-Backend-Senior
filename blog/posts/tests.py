from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User, Profile
from .models import Post, Tag, Comment, Like
from faker import Faker
fake = Faker()


########################################################################
class PostAndTagTestCase(TestCase):

    # ----------------------------------------------------------------------
    def setUp(self):
        self.author = User.objects.create_user(username=fake.unique.user_name(), password='testpass')
        Profile.objects.create(user=self.author, bio='test bio')

        self.post = Post.objects.create(author=self.author, title='title', content='content', category='category')
        self.post_to_delete_1 = Post.objects.create(author=self.author, title='title', content='content', category='category')
        self.post_to_delete_2 = Post.objects.create(author=self.author, title='title', content='content', category='category')
        self.post_to_delete_3 = Post.objects.create(author=self.author, title='title', content='content', category='category')

        self.clients = {}
        for role in ['admin', 'editor', 'blogger']:
            client = APIClient()
            test_user = User.objects.create_user(username=fake.unique.user_name(), password='testpass', role=role)
            Profile.objects.create(user=test_user, bio='test bio')
            self.refresh = RefreshToken.for_user(test_user)
            client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
            self.clients[role] = client

        client = APIClient()
        self.refresh = RefreshToken.for_user(self.author)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.clients['author'] = client

    # ----------------------------------------------------------------------
    def test_create_post(self):
        post_count = Post.objects.count()
        tag_count = Tag.objects.count()

        tag_data = ['tag1', 'tag2', 'tag3']
        new_post_data = {'author_id': self.author.id,
                         'title': fake.sentence(),
                         'content': fake.text(),
                         'category': fake.word(),
                         'tags': tag_data,
                         }

        response = self.clients['admin'].post('/posts/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(Tag.objects.count(), tag_count + 3)

        response = self.clients['editor'].post('/posts/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), post_count + 2)
        self.assertEqual(Tag.objects.count(), tag_count + 3)

        response = self.clients['blogger'].post('/posts/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), post_count + 3)
        self.assertEqual(Tag.objects.count(), tag_count + 3)

    # ----------------------------------------------------------------------
    def test_read_posts(self):
        response = self.clients['admin'].get(f'/posts/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['editor'].get(f'/posts/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['blogger'].get(f'/posts/', format='json')
        self.assertEqual(response.status_code, 200)

    # ----------------------------------------------------------------------
    def test_read_post(self):
        response = self.clients['admin'].get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['admin'].get(f'/posts/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['editor'].get(f'/posts/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].get(f'/posts/{self.post.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['blogger'].get(f'/posts/999999999/')
        self.assertEqual(response.status_code, 404)

    # ----------------------------------------------------------------------
    def test_update_post(self):
        tag_data = ['tag4', 'tag5', 'tag6']
        new_post_data = {'title': fake.sentence(), 'tags': tag_data}

        response = self.clients['admin'].patch(f'/posts/{self.post.id}/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.clients['admin'].patch(f'/posts/999999999/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].patch(f'/posts/{self.post.id}/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.clients['editor'].patch(f'/posts/999999999/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].patch(f'/posts/{self.post.id}/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 403)
        response = self.clients['author'].patch(f'/posts/{self.post.id}/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.clients['blogger'].patch(f'/posts/999999999/', data=new_post_data, format='json')
        self.assertEqual(response.status_code, 404)

    # ----------------------------------------------------------------------
    def test_delete_post(self):
        post_count = Post.objects.count()

        response = self.clients['admin'].delete(f'/posts/{self.post_to_delete_1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), post_count - 1)
        response = self.clients['admin'].delete(f'/posts/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].delete(f'/posts/{self.post_to_delete_2.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), post_count - 2)
        response = self.clients['editor'].delete(f'/posts/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].delete(f'/posts/{self.post_to_delete_3.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), post_count - 2)
        response = self.clients['author'].delete(f'/posts/{self.post_to_delete_3.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), post_count - 3)
        response = self.clients['blogger'].delete(f'/posts/999999999/', format='json')
        self.assertEqual(response.status_code, 404)


########################################################################
class CommentTestCase(TestCase):

    # ----------------------------------------------------------------------
    def setUp(self):
        self.author = User.objects.create_user(username=fake.unique.user_name(), password='testpass')
        Profile.objects.create(user=self.author, bio='test bio')

        self.post = Post.objects.create(author=self.author, title='title', content='content', category='category')

        self.comment = Comment.objects.create(user=self.author, post=self.post, text='text')

        self.comment_to_delete_1 = Comment.objects.create(user=self.author, post=self.post, text='text')
        self.comment_to_delete_2 = Comment.objects.create(user=self.author, post=self.post, text='text')
        self.comment_to_delete_3 = Comment.objects.create(user=self.author, post=self.post, text='text')

        self.clients = {}
        for role in ['admin', 'editor', 'blogger']:
            client = APIClient()
            test_user = User.objects.create_user(username=fake.unique.user_name(), password='testpass', role=role)
            Profile.objects.create(user=test_user, bio='test bio')
            self.refresh = RefreshToken.for_user(test_user)
            client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
            self.clients[role] = client

        client = APIClient()
        self.refresh = RefreshToken.for_user(self.author)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.clients['author'] = client

    # ----------------------------------------------------------------------
    def test_create_comment(self):
        comment_count = Comment.objects.count()

        new_comment_data = {'user_id': self.author.id,
                            'post_id': self.post.id,
                            'text': fake.text(),
                            }

        response = self.clients['admin'].post('/comments/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), comment_count + 1)

        response = self.clients['editor'].post('/comments/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), comment_count + 2)

        response = self.clients['blogger'].post('/comments/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), comment_count + 3)

    # ----------------------------------------------------------------------
    def test_read_comments(self):
        response = self.clients['admin'].get(f'/comments/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['editor'].get(f'/comments/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['blogger'].get(f'/comments/', format='json')
        self.assertEqual(response.status_code, 200)

    # ----------------------------------------------------------------------
    def test_read_comment(self):
        response = self.clients['admin'].get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['admin'].get(f'/comments/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['editor'].get(f'/comments/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].get(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['blogger'].get(f'/comments/999999999/')
        self.assertEqual(response.status_code, 404)

    # ----------------------------------------------------------------------
    def test_update_comment(self):
        new_comment_data = {'id': self.comment.id, 'text': fake.text(), }

        response = self.clients['admin'].patch(f'/comments/{self.comment.id}/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.clients['admin'].patch(f'/comments/999999999/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].patch(f'/comments/{self.comment.id}/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.clients['editor'].patch(f'/comments/999999999/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].patch(f'/comments/{self.comment.id}/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 403)
        response = self.clients['author'].patch(f'/comments/{self.comment.id}/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.clients['blogger'].patch(f'/comments/999999999/', data=new_comment_data, format='json')
        self.assertEqual(response.status_code, 404)

    # ----------------------------------------------------------------------
    def test_delete_comment(self):
        comment_count = Comment.objects.count()

        response = self.clients['admin'].delete(f'/comments/{self.comment_to_delete_1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), comment_count - 1)
        response = self.clients['admin'].delete(f'/comments/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].delete(f'/comments/{self.comment_to_delete_2.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), comment_count - 2)
        response = self.clients['editor'].delete(f'/comments/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].delete(f'/comments/{self.comment_to_delete_3.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Comment.objects.count(), comment_count - 2)
        response = self.clients['author'].delete(f'/comments/{self.comment_to_delete_3.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), comment_count - 3)
        response = self.clients['blogger'].delete(f'/comments/999999999/', format='json')
        self.assertEqual(response.status_code, 404)


########################################################################
class LikeTestCase(TestCase):

    # ----------------------------------------------------------------------
    def setUp(self):
        self.author = User.objects.create_user(username=fake.unique.user_name(), password='testpass')
        Profile.objects.create(user=self.author, bio='test bio')

        self.post = Post.objects.create(author=self.author, title='title', content='content', category='category')
        self.like = Like.objects.create(user=self.author, post=self.post)

        self.like_to_delete_1 = Like.objects.create(user=self.author, post=self.post)
        self.like_to_delete_2 = Like.objects.create(user=self.author, post=self.post)
        self.like_to_delete_3 = Like.objects.create(user=self.author, post=self.post)

        # self.comment = Comment.objects.create(user=self.author, post=self.post, text='text')

        # self.comment_to_delete_1 = Comment.objects.create(user=self.author, post=self.post, text='text')
        # self.comment_to_delete_2 = Comment.objects.create(user=self.author, post=self.post, text='text')
        # self.comment_to_delete_3 = Comment.objects.create(user=self.author, post=self.post, text='text')

        self.clients = {}
        for role in ['admin', 'editor', 'blogger']:
            client = APIClient()
            test_user = User.objects.create_user(username=fake.unique.user_name(), password='testpass', role=role)
            Profile.objects.create(user=test_user, bio='test bio')
            self.refresh = RefreshToken.for_user(test_user)
            client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
            self.clients[role] = client

        client = APIClient()
        self.refresh = RefreshToken.for_user(self.author)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        self.clients['author'] = client

    # ----------------------------------------------------------------------
    def test_create_like(self):
        like_count = Like.objects.count()

        new_like_data = {'user_id': self.author.id,
                         'post': self.post.id,
                         }

        response = self.clients['admin'].post('/likes/', data=new_like_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.count(), like_count + 1)

        response = self.clients['editor'].post('/likes/', data=new_like_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.count(), like_count + 2)

        response = self.clients['blogger'].post('/likes/', data=new_like_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.count(), like_count + 3)

    # ----------------------------------------------------------------------
    def test_read_likes(self):
        response = self.clients['admin'].get(f'/likes/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['editor'].get(f'/likes/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['blogger'].get(f'/likes/', format='json')
        self.assertEqual(response.status_code, 200)

    # ----------------------------------------------------------------------
    def test_read_like(self):
        response = self.clients['admin'].get(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['admin'].get(f'/likes/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].get(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['editor'].get(f'/likes/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].get(f'/likes/{self.like.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['blogger'].get(f'/likes/999999999/')
        self.assertEqual(response.status_code, 404)

    # ----------------------------------------------------------------------
    def test_delete_like(self):
        like_count = Like.objects.count()

        response = self.clients['admin'].delete(f'/likes/{self.like_to_delete_1.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Like.objects.count(), like_count - 1)
        response = self.clients['admin'].delete(f'/likes/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].delete(f'/likes/{self.like_to_delete_2.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Like.objects.count(), like_count - 2)
        response = self.clients['editor'].delete(f'/likes/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].delete(f'/likes/{self.like_to_delete_3.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Like.objects.count(), like_count - 2)
        response = self.clients['author'].delete(f'/likes/{self.like_to_delete_3.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Like.objects.count(), like_count - 3)
        response = self.clients['blogger'].delete(f'/likes/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

