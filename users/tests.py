''' Unit tests for the users application. '''
from django.test import TestCase
from django.urls import reverse
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


class UsersViewsTestCase(TestCase):
    ''' Unit tests for users application views '''
    def setUp(self):
        '''
        Creating a test user and log in for authentication purposes
        '''
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        '''
        Testing that the home view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')

    def test_about_view(self):
        '''
        Testing that the about view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/about.html')

    def test_help_view(self):
        '''
        Testing that the help view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/help.html')

    def test_dashboard_view(self):
        '''
        Testing that the dashboard view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/dashboard.html')

    def test_sign_up_view(self):
        '''
        Testing that the sign-up view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('signUp'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signUp.html')


    def test_sign_in_view(self):
        '''
        Testing that the sign-in view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('signIn'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/signIn.html')


    def test_log_out_view(self):
        '''
        Testing that the log-out view redirects to the home page after logout
        '''
        response = self.client.get(reverse('logOut'))
        self.assertEqual(response.status_code, 302)  # Redirects to home after logout

    def test_profile_view(self):
        '''
        Testing that the profile view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('profile', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_settings_view(self):
        '''
        Testing that the settings view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/settings.html')

    def test_custom_password_change_view(self):
        '''
        Testing that the custom password change view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('custom_password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')

    def test_custom_password_change_done_view(self):
        '''
        Testing that the custom password change done view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('custom_password_change_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_done.html')

    def test_deactivate_account_view(self):
        '''
        Testing that the deactivate account view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('deactivate_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/deactivate_account.html')

    def test_account_deactivated_view(self):
        '''
        Testing that the account deactivated view redirects to the home page after deactivation
        '''
        response = self.client.get(reverse('account_deactivated'))
        self.assertEqual(response.status_code, 302)  # Redirects to home after deactivation

    def test_search_view(self):
        '''
        Testing that the search view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/search_results.html')

    def test_notifications_view(self):
        '''
        Testing that the notifications view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/notifications.html')

    def test_reminders_view(self):
        '''
        Testing that the reminders view returns a status code of 200 and uses the correct template
        '''
        response = self.client.get(reverse('reminders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/reminders.html')