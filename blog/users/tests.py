from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User, Profile
from faker import Faker
fake = Faker()


########################################################################
class JWTAuthTestCase(TestCase):

    # ----------------------------------------------------------------------
    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.create_user(username=fake.unique.user_name(), password='testpass')
        self.test_profile = Profile.objects.create(user=self.test_user, bio='test bio')
        self.refresh = RefreshToken.for_user(self.test_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')

    # ----------------------------------------------------------------------
    def test_jwt_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer wrongtoken')
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 401)  # Unauthorized

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)  # OK


########################################################################
class UserAndProfileTestCase(TestCase):

    # ----------------------------------------------------------------------
    def setUp(self):
        self.user_to_delete = User.objects.create_user(username=fake.unique.user_name(), password='testpass')
        Profile.objects.create(user=self.user_to_delete, bio='test bio')

        self.user_to_inspect = User.objects.create_user(username=fake.unique.user_name(), password='testpass')
        Profile.objects.create(user=self.user_to_inspect, bio='test bio')

        self.clients = {}
        for role in ['admin', 'editor', 'blogger']:
            client = APIClient()
            test_user = User.objects.create_user(username=fake.unique.user_name(), password='testpass', role=role)
            Profile.objects.create(user=test_user, bio='test bio')
            self.refresh = RefreshToken.for_user(test_user)
            client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.refresh.access_token}')
            self.clients[role] = client

    # ----------------------------------------------------------------------
    def test_create_user_and_profile(self):
        user_count = User.objects.count()
        profile_count = Profile.objects.count()
        profile_data = {'bio': 'New bio'}
        new_user_data = {'username': fake.unique.user_name(), 'password': 'newpass', 'profile': profile_data, }

        response = self.clients['admin'].post('/users/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertEqual(Profile.objects.count(), profile_count + 1)

        response = self.clients['editor'].post('/users/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertEqual(Profile.objects.count(), profile_count + 1)

        response = self.clients['blogger'].post('/users/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertEqual(Profile.objects.count(), profile_count + 1)

    # ----------------------------------------------------------------------
    def test_read_users_and_profile(self):
        response = self.clients['admin'].get(f'/users/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['editor'].get(f'/users/', format='json')
        self.assertEqual(response.status_code, 200)

        response = self.clients['blogger'].get(f'/users/', format='json')
        self.assertEqual(response.status_code, 200)

    # ----------------------------------------------------------------------
    def test_read_user_and_profile(self):
        response = self.clients['admin'].get(f'/users/{self.user_to_inspect.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['admin'].get(f'/users/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].get(f'/users/{self.user_to_inspect.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['editor'].get(f'/users/999999999/')
        self.assertEqual(response.status_code, 404)

        response = self.clients['blogger'].get(f'/users/{self.user_to_inspect.id}/')
        self.assertEqual(response.status_code, 200)
        response = self.clients['blogger'].get(f'/users/999999999/')
        self.assertEqual(response.status_code, 404)

    # ----------------------------------------------------------------------
    def test_update_user_and_profile(self):
        profile_data = {'bio': 'New updated bio'}
        new_user_data = {'username': fake.unique.user_name(), 'profile': profile_data, }

        response = self.clients['admin'].patch(f'/users/{self.user_to_inspect.id}/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.clients['admin'].patch(f'/users/999999999/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].patch(f'/users/{self.user_to_inspect.id}/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 403)
        response = self.clients['editor'].patch(f'/users/999999999/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 403)

        response = self.clients['blogger'].patch(f'/users/{self.user_to_inspect.id}/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 403)
        response = self.clients['blogger'].patch(f'/users/999999999/', data=new_user_data, format='json')
        self.assertEqual(response.status_code, 403)

    # ----------------------------------------------------------------------
    def test_delete_user_and_profile(self):
        user_count = User.objects.count()
        profile_count = Profile.objects.count()

        response = self.clients['admin'].delete(f'/users/{self.user_to_delete.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), user_count - 1)
        self.assertEqual(Profile.objects.count(), profile_count - 1)
        response = self.clients['admin'].delete(f'/users/999999999/', format='json')
        self.assertEqual(response.status_code, 404)

        response = self.clients['editor'].delete(f'/users/{self.user_to_delete.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), user_count - 1)
        self.assertEqual(Profile.objects.count(), profile_count - 1)
        response = self.clients['editor'].delete(f'/users/999999999/', format='json')
        self.assertEqual(response.status_code, 403)

        response = self.clients['blogger'].delete(f'/users/{self.user_to_delete.id}/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), user_count - 1)
        self.assertEqual(Profile.objects.count(), profile_count - 1)
        response = self.clients['blogger'].delete(f'/users/999999999/', format='json')
        self.assertEqual(response.status_code, 403)

