''' Unit tests for the users application. '''
from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType
from .models import Profile
# from django.core import mail
# from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


# # Create your tests here.

#Testing User Creation
class UserCreationTestCase(TestCase):
    ''' Testing the creation of the User model. '''
    def test_create_user(self):
        '''  Test ensures that a User object can be created correctly. '''
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

#Testing User Authentication
class UserAuthenticationTestCase(TestCase):
    ''' Testing the authentication of the user model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_login_valid_user(self):
        ''' Tests ensures valid users can sign in successfully. '''
        response= self.client.login(username='testuser', password='testpassword')
        self.assertTrue(response)

    def test_login_invalid_user(self):
        ''' Tests ensures invalid users cannot sign in. '''
        response = self.client.login(username='testuser', password='wrongpassword')


class ProfileModelTest(TestCase):
    ''' Tests the creation and string representation of the Profile model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(
            user=self.user,
            date_of_birth='1990-01-01',
            profile_picture='profile_pics/test.jpg'
        )

    def test_profile_creation(self):
        '''  Test ensures that a Profile object can be created correctly. '''
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(str(self.profile.date_of_birth), '1990-01-01')
        self.assertEqual(self.profile.profile_picture, 'profile_pics/test.jpg')

    def test_profile_str(self):
        ''' Test verifies if the string representation of a Profile object is correct. '''
        expected_str = self.user.username
        self.assertEqual(str(self.profile), expected_str)
