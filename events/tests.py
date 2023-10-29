''' Unit tests for the events application. '''
from django.test import TestCase
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