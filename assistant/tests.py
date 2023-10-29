'''
    Script containing unit tests for the assistant application.
'''
from django.test import TestCase
from django.contrib.auth.models import User
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