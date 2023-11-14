''' Unit tests for the broadcasts application. '''
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Broadcast
from circle.models import Member, Group

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


class BroadcastViewsTestCase(TestCase):
    ''' Test cases for broadcast application views. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def create_broadcast(self, title='Test Broadcast', content='Test Content', is_draft=False):
        return Broadcast.objects.create(
            user=self.user,
            title=title,
            content=content,
            is_draft=is_draft
        )
    
    def test_broadcast_list_view(self):
        ''' Checking if the broadcast_list view returns a 200 OK status. '''
        response = self.client.get(reverse('broadcast_list'))
        self.assertEqual(response.status_code, 200)

    def test_sent_broadcast_list_view(self):
        '''  Checking if the sent_broadcast_list view returns a 200 OK status. '''
        response = self.client.get(reverse('sent_broadcast_list'))
        self.assertEqual(response.status_code, 200)

    def test_draft_broadcast_list_view(self):
        ''' Checking if the draft_broadcast_list view returns a 200 OK status. '''
        response = self.client.get(reverse('draft_broadcast_list'))
        self.assertEqual(response.status_code, 200)

    def test_broadcast_detail_view(self):
        ''' Checking if the broadcast_detail view returns a 200 OK status. '''
        broadcast = self.create_broadcast()
        response = self.client.get(reverse('broadcast_detail', args=[broadcast.id]))
        self.assertEqual(response.status_code, 200)

    def assertRedirect(self, response, expected_url):
        self.assertEqual(response.status_code, 302, f"Expected a redirect, but got {response.status_code}.")
        self.assertEqual(response.url, expected_url, f"Expected redirect to {expected_url}, but got {response.url}.")

    def test_create_broadcast_view(self):
        '''  Checking if the create_broadcast view successfully redirects after submitting a new broadcast form. '''
        response = self.client.post(reverse('create_broadcast'), {'title': 'New Broadcast', 'content': 'New Content'})
        if response.status_code != 302:
            print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission

    def test_send_broadcast_draft_view(self):
        ''' Checking if the send_broadcast_draft view successfully redirects after sending a draft. '''
        draft = self.create_broadcast(is_draft=True)
        response = self.client.get(reverse('send_broadcast_draft', args=[draft.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after sending the draft

    def test_edit_broadcast_view(self):
        '''  Checking if the edit_broadcast view successfully redirects after editing a broadcast. '''
        broadcast = self.create_broadcast()
        response = self.client.post(reverse('edit_broadcast', args=[broadcast.id]), {'title': 'Updated Title'})
        if response.status_code != 302:
            print(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 302)  # Redirects after successful form submission

    def test_delete_broadcast_view(self):
        ''' Checking if the delete_broadcast view successfully redirects after deleting a broadcast. '''
        broadcast = self.create_broadcast()
        response = self.client.post(reverse('delete_broadcast', args=[broadcast.id]))
        self.assertEqual(response.status_code, 302)  # Redirects after successful deletion

    def test_read_broadcast_view(self):
        '''  Checking if the read_broadcast view returns a 200 OK status. '''
        user = User.objects.create_user(username='testuser', password='testpassword')
        member = Member.objects.create(name='Test Member', user=user)
        broadcast = self.create_broadcast()
        response = self.client.get(reverse('read_broadcast', args=[broadcast.id, member.id]))
        self.assertEqual(response.status_code, 200)