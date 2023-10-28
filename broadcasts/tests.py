''' Unit tests for the broadcasts application. '''
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Broadcast
from circle.models import Member

# Create your tests here.
class BroadcastModelTest(TestCase):
    ''' Test cases for the Broadcast model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test User',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.broadcast = Broadcast.objects.create(
            user=self.user,
            title='Test Broadcast',
            content='Test Content',
            is_draft=True
        )
        self.broadcast.receivers.add(self.member)

    def test_broadcast_creation(self):
        ''' Testing the creation of a new Broadcast object. '''
        self.assertEqual(self.broadcast.title, 'Test Broadcast')
        self.assertEqual(self.broadcast.content, 'Test Content')
        self.assertTrue(self.broadcast.is_draft)
        self.assertEqual(self.broadcast.receivers.count(), 1)

    def test_broadcast_str(self):
        ''' Testing that the string value of a broadcast object is the broadcast.title '''
        self.assertEqual(str(self.broadcast), 'Test Broadcast')

    def test_broadcast_receivers(self):
        '''Testing if the receiver is associated correctly with the broadcast'''
        self.assertEqual(self.broadcast.receivers.first(), self.member)