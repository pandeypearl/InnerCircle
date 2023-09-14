from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.test.client import Client
from django.contrib.contenttypes.models import ContentType
from users.models import Profile
from django.core import mail
from django.urls import reverse

# Create your tests here.

#Testing User Creation
class UserCreationTestCase(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

#Testing User Authentication
class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    def test_login_valid_user(self):
        response= self.client.login(username='testuser', password='testpassword')
        self.assertTrue(response)

    def test_login_invalid_user(self):
        response = self.client.login(username='testuser', password='wrongpassword')

#Testing User Permission
class UserPermissionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        content_type = ContentType.objects.get_for_model(Profile)
        permission = Permission.objects.get(content_type=content_type, codename='can_view')
        self.user.user_permissions.add(permission)

    def test_user_has_permission(self):
        self.assertTrue(self.user.has_perm('users.can_view'))

    def test_user_does_not_have_permission(self):
        self.assertFalse(self.user.has_perm('users.can_edit'))

#Testing Password Reset
class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_password_reset_view(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_email_sent(self):
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)

#Testing Forgotten Password
class ForgottenPasswordTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_forgotten_password_view(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_forgotten_password_email_sent(self):
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Password reset', email.subject)
        self.assertIn('To reset your password', email.body)
        reset_link_start = email.body.find('http://')
        reset_link_end = email.body.find('/reset/')
        reset_link = email.body[reset_link_start:reset_link_end]
        reset_response = self.client.get(reset_link)
        self.assertEqual(reset_response.status_code, 200)

    def test_reset_password(self):
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})
        email = mail.outbox[0]
        reset_link_start = email.body.find('http://')
        reset_link_end = email.body.find('/reset/')
        reset_link = email.body[reset_link_start:reset_link_end]
        reset_response = self.client.get(reset_link, {'new_password1': 'newpassword', 'new_password2': 'new_password'})
        self.assertEqual(reset_response.status_code, 302)
        self.assertTrue(self.client.login(username='testuser', password='newpassword'))
