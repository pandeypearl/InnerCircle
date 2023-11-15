''' Unit tests for the events application. '''
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from circle.models import Member
from .models import Event, RSVP, RSVPNotification
from django.utils import timezone

# Create your tests here.
class EventModelTest(TestCase):
    ''' Tests the creation and string representation of the Event model. '''
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.event = Event.objects.create(
            user=self.user,
            event_name='Test Event',
            description='Test Description',
            date='2023-10-29 12:00:00+00:00',
            location='Test Location',
            dress_code='Casual'
        )
        self.event.guests.add(self.member)

    def test_event_creation(self):
        self.assertEqual(self.event.event_name, 'Test Event')
        self.assertEqual(self.event.description, 'Test Description')
        self.assertEqual(str(self.event.date), '2023-10-29 12:00:00+00:00')
        self.assertEqual(self.event.location, 'Test Location')
        self.assertEqual(self.event.dress_code, 'Casual')
        self.assertEqual(self.event.guests.count(), 1)

    def test_event_str(self):
        self.assertEqual(str(self.event), 'Test Event')


class RSVPModelTest(TestCase):
    ''' Tests the creation and string representation of the RSVP model. '''
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.event = Event.objects.create(
            user=self.user,
            event_name='Test Event',
            description='Test Description',
            date=timezone.now(),
            location='Test Location',
            dress_code='Casual'
        )
        self.event.guests.add(self.member)
        self.rsvp=RSVP.objects.create(
            event=self.event,
            guest=self.member,
            response_status='Attending',
            guest_count=2,
            dietary_preferences='None'
        )

    def test_rsvp_creation(self):
        self.assertEqual(self.rsvp.event, self.event)
        self.assertEqual(self.rsvp.guest, self.member)
        self.assertEqual(self.rsvp.response_status, 'Attending')
        self.assertEqual(self.rsvp.dietary_preferences, 'None')
        self.assertEqual(self.event.guests.count(), 1)

    def test_rsvp_str(self):
        self.assertEqual(str(self.rsvp), 'Test Member RSVP for Test Event')


class RSVPNotificationModelTest(TestCase):
    ''' Tests the creation and created_at attribute of the RSVPNotification model '''
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.event = Event.objects.create(
            user=self.user,
            event_name='Test Event',
            description='Test Description',
            date='2023-10-30T12:00:00Z',
            location='Test Location',
            dress_code='Casual'
        )
        self.rsvp=RSVP.objects.create(
            event=self.event,
            guest=self.member,
            response_status='Attending',
            guest_count=2,
            dietary_preferences='None'
        )
        self.notification = RSVPNotification.objects.create(
            user=self.user,
            event=self.event,
            rsvp=self.rsvp
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.event, self.event)
        self.assertEqual(self.notification.rsvp, self.rsvp)

    def test_notification_created_at(self):
        self.assertIsNotNone(self.notification.created_at)


class EventViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_event_list_view(self):
        '''
        Checking whether the 'event_list' view is accessible by a logged-in user
        and verifying that the HTTP response status code is 200.
        '''
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)

    def test_sent_event_list_view(self):
        '''
        Ensuring that the 'sent_event_list' view is accessible by a logged-in user
        and confirming that the HTTP response status code is 200.
        '''
        response = self.client.get(reverse('sent_event_list'))
        self.assertEqual(response.status_code, 200)

    def test_draft_event_list_view(self):
        '''
        Validating that the 'draft_event_list' view is accessible by a logged-in user
        and checking that the HTTP response status code is 200.
        '''
        response = self.client.get(reverse('draft_event_list'))
        self.assertEqual(response.status_code, 200)

    def test_event_detail_view(self):
        '''
        Verifying that the 'event_detail' view displays detailed information about a specific event 
        and checking that the HTTP response status code is 200.
        '''
        event = Event.objects.create(user=self.user, event_name='Test Event', date='2023-01-01')
        response = self.client.get(reverse('event_detail', args=[event.id]))
        self.assertEqual(response.status_code, 200)

    def test_create_event_view(self):
        '''
        Checking the accessibility of the 'create_event' view, ensuring that the form submission process works as expected
        and validating that the HTTP response status code is 200 for the initial view and 302 after a successful form submission.
        '''
        event = Event.objects.create(user=self.user, event_name='Test Event', date=timezone.now())
        response = self.client.get(reverse('create_event'))
        self.assertEqual(response.status_code, 200)
        # Test form submission
        response = self.client.post(reverse('create_event'), data={'event_name': 'Test Event'})
        self.assertEqual(response.status_code, 302)  # Redirect after form submission

    def test_send_event_draft_view(self):
        '''
        Confirming that the 'send_event_draft' view correctly sends invitations for a draft event
        and checking that the HTTP response status code is 302 after sending the draft.
        '''
        draft = Event.objects.create(user=self.user, event_name='Test Draft', is_draft=True, date=timezone.now())
        response = self.client.get(reverse('send_event_draft', args=[draft.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after sending draft

    def test_update_event_view(self):
        '''
        Ensuring that the 'update_event' view is accessible and that the form submission process for updating an event works as expected.
        Validating that the HTTP response status code is 200 for the initial view and 302 after a successful form submission.
        '''
        event = Event.objects.create(user=self.user, event_name='Test Event', date=timezone.now())
        response = self.client.get(reverse('update_event', args=[event.id]))
        self.assertEqual(response.status_code, 200)
        # Test form submission
        response = self.client.post(reverse('update_event', args=[event.id]), data={'event_name': 'Updated Event'})
        self.assertEqual(response.status_code, 302)  # Redirect after form submission


    def test_delete_event_view(self):
        '''
        Checking the accessibility of the 'delete_event' view and verifying that the deletion process for an event is successful.
        Confirming that the HTTP response status code is 200 for the initial view and 302 after a successful event deletion.
        '''
        event = Event.objects.create(user=self.user, event_name='Test Event', date='2023-01-01')
        response = self.client.get(reverse('delete_event', args=[event.id]))
        self.assertEqual(response.status_code, 200)
        # Test form submission
        response = self.client.post(reverse('delete_event', args=[event.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after form submission


    def test_rsvp_view(self):
        '''
        Checking the accessibility of the 'rsvp_view' for a specific event and member
        and validating the RSVP form submission process, ensuring that the HTTP response status code is 200 
        for the initial view and 302 after a successful form submission.
        '''
        event = Event.objects.create(user=self.user, event_name='Test Event', date=timezone.now())
        member = Member.objects.create(user=self.user, name='Test Member')
        response = self.client.get(reverse('rsvp_view', args=[event.id, member.id]))
        self.assertEqual(response.status_code, 200)
        # Test form submission
        response = self.client.post(reverse('rsvp_view', args=[event.id, member.id]), data={'response_status': 'Attending'})
        self.assertEqual(response.status_code, 302)  # Redirect after form submission


    def test_rsvp_done_view(self):
        '''
        Verifying that the 'rsvp_done_view' displays a confirmation message after a member submits their RSVP response for a specific event 
        and checking that the HTTP response status code is 200.
        '''
        event = Event.objects.create(user=self.user, event_name='Test Event', date=timezone.now())
        member = Member.objects.create(user=self.user, name='Test Member')
        response = self.client.get(reverse('rsvp_done', args=[event.id, member.id]))
        self.assertEqual(response.status_code, 200)
