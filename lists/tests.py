from django.test import TestCase
from django.contrib.auth.models import User
from circle.models import Member
from .models import List, ListItem, CheckItem, CheckItemNotification 

# Create your tests here.
class ListModelTest(TestCase):
    ''' Tests the creation and string representation of the List model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.list = List.objects.create(
            user=self.user,
            list_name='Test List',
            description='Test Description',
            is_draft=True
        )
        self.list.receivers.add(self.member)

    def test_list_creation(self):
        ''' Test ensures that a List object can be created correctly. '''
        self.assertEqual(self.list.list_name, 'Test List')
        self.assertEqual(self.list.description, 'Test Description')
        self.assertTrue(self.list.is_draft, 'Test Description')
        self.assertTrue(self.list.receivers.count(), 1)

    def test_list_str(self):
        ''' Test checks if the string representation of a List object is correct. '''
        self.assertEqual(str(self.list), 'Test List')


class ListItemModelTest(TestCase):
    ''' Tests the creation and string representation of the ListItem model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.list = List.objects.create(
            user=self.user,
            list_name='Test List',
            description='Test Description',
            is_draft=True
        )
        self.list_item = ListItem.objects.create(
            list=self.list,
            item_name='Test Item',
            item_url='http://example.com/test'
        )

    def list_item_creation(self):
        ''' Test verifies the creation of a ListItem object. '''
        self.assertEqual(self.list_item.item_name, 'Test Item')
        self.assertEqual(self.list_item.item_url, 'http://example.com/test')
        self.assertFalse(self.list_item.checked)

    def test_list_item_str(self):
        '''  Test ensures that the string representation of a ListItem object is correct. '''
        self.assertEqual(str(self.list_item), 'Test Item')


class CheckItemModelTest(TestCase):
    ''' Tests the creation and string representation of the CheckItem model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.list = List.objects.create(
            user=self.user,
            list_name='Test List',
            description='Test Description',
            is_draft=True
        )
        self.list_item = ListItem.objects.create(
            list=self.list,
            item_name='Test Item',
            item_url='http://example.com/test',
        )
        self.check_item = CheckItem.objects.create(
            item=self.list_item,
            recipient=self.member
        )

    def test_check_item_creation(self):
        ''' Test checks if a CheckItem object can be created successfully.
            Verifies if the relationships with ListItem and Member are correctly established.
        '''
        self.assertEqual(self.check_item.item, self.list_item)
        self.assertEqual(self.check_item.recipient, self.member)

    def test_check_item_str(self):
        '''  Test validates if the string representation of a CheckItem object is accurate. '''
        expected_str = f"{self.member.name} checked {self.list_item}  at {self.check_item.checked_at}"
        self.assertEqual(str(self.check_item), expected_str)


class CheckItemNotificationModelTest(TestCase):
    ''' Tests the creation and created_at field of the CheckItem model. '''
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@example.com',
            relationship='Test Relationship'
        )
        self.list = List.objects.create(
            user=self.user,
            list_name='Test List',
            description='Test Description',
            is_draft=True
        )
        self.list_item = ListItem.objects.create(
            list=self.list,
            item_name='Test Item',
            item_url='http://example.com/test',
        )
        self.check_item = CheckItem.objects.create(
            item=self.list_item,
            recipient=self.member
        )
        self.notification = CheckItemNotification.objects.create(
            user=self.user,
            list_item=self.list_item,
            check_item=self.check_item
        )

    def test_notification_creation(self):
        ''' Test ensures that a CheckItemNotification object is created correctly.
            Checks if the relationships with User, ListItem, CheckItem, and List are correctly set.
        '''
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.list_item, self.list_item)
        self.assertEqual(self.notification.check_item, self.check_item)
        self.assertEqual(self.notification.list_reference, self.list)

    def test_notification_created_at(self):
        ''' Test checks if the created_at field of a CheckItemNotification object is not empty. '''
        self.assertIsNotNone(self.notification.created_at)