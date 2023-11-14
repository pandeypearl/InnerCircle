'''
    Script containing unit tests for the assistant application.
'''
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Chat

# Create your tests here.
class ChatModelTest(TestCase):
    ''' Tests the creation, created_at and string representation of the List model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.chat = Chat.objects.create(
            user=self.user,
            message='Test message',
            response='Test response'
        )

    def test_chat_creation(self):
        ''' Test ensures that a Chat object can be created correctly.'''
        self.assertEqual(self.chat.user, self.user)
        self.assertEqual(self.chat.message, 'Test message')
        self.assertEqual(self.chat.response, 'Test response')

    def test_chat_str(self):
        '''  Test verifies if the string representation of a Chat object is correct. '''
        expected_str = f"{self.user.username}: Test message"
        self.assertEqual(str(self.chat), expected_str)

    def test_chat_created_at(self):
        '''  Test checks if the created_at field of a Chat object is not empty.  '''
        self.assertIsNotNone(self.chat.created_at)


class AssistantViewsTest(TestCase):
    ''' Tests the assistant, chat_history and unavailable views of the Assistant Application '''
    def setUp(self):
        ''' Creating a superuser for testing '''
        self.user = User.objects.create_user(username='testuser', password='testpassword', is_superuser=True)
        self.client = Client()

    def test_assistant_view(self):
        ''' Logging in the user and testing the assistant view with GET and POST requests '''
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(reverse('assistant'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/assistant.html')

        response = self.client.post(reverse('assistant'), {'message': 'Hello, OpenAI!'})
        self.assertEqual(response.status_code, 200)
        actual_response = response.json()
        expected_response = {'message': 'Hello, OpenAI!', 'response': actual_response['response']}
        self.assertJSONEqual(response.content, expected_response)

    def test_chat_history_view(self):
        ''' Logging in user, creating a chat for the user, and testing the chat history view. '''
        self.client.login(username='testuser', password='testpassword')

        Chat.objects.create(user=self.user, message='Test message', response='Test response')

        response = self.client.get(reverse('chat_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/chat_history.html')
        self.assertContains(response, 'Test message')
        self.assertContains(response, 'Test response')

    def test_unavailable_feature_view(self):
        ''' Logging in user and testing unavailable feature view. '''
        self.client.login(username='testuser', password='testpassword')
        
        response = self.client.get(reverse('unavailable_feature'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assistant/unavailable_feature.html')

    def test_assistant_view_redirect_non_superuser(self):
        ''' Creating a regular user for testing and testing assistant view redirection for non-superuser '''
        regular_user = User.objects.create_user(username='regularuser', password='testpassword', is_superuser=False)
        self.client.login(username='regularuser', password='testpassword')

        response = self.client.get(reverse('assistant'))
        self.assertEqual(response.status_code, 302) # Expecting a redirect status code

    def test_chat_history_view_redirect_non_superuser(self):
        ''' Creating a regular user for testing and testing chat history view redirection for non-superuser '''
        regular_user = User.objects.create_user(username='regularuser', password='testpassword', is_superuser=False)
        self.client.login(username='regularuser', password='testpassword')

        response = self.client.get(reverse('chat_history'))
        self.assertEqual(response.status_code, 302)  # Expecting a redirect status code

   
