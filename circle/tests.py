''' Unit tests for the circle application. '''
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Member, Group, Note


# Create your tests here.
class MemberModelTest(TestCase):
    ''' Test cases for the Member model. '''
    def setUp(self):
        ''' Setting up data for Member model tests'''
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )

    def test_member_creation(self):
        ''' Testing the creation of a new member object. '''
        self.assertEqual(self.member.name, 'Test Member')
        self.assertEqual(self.member.email, 'test@testemail.com')
        self.assertEqual(self.member.relationship, 'Test Relationship')

    def test_member_str(self):
        ''' Testing that the string value of a member object is the member.name '''
        self.assertEqual(str(self.member), 'Test Member')


class GroupModelTest(TestCase):
    ''' test cases for the Group model. '''
    def setUp(self):
        ''' Setting up data for Group model tests'''
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(
            user=self.user,
            group_name='Test Group',
            description='Test Description'
        )
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.group.members.add(self.member)

    def test_group_creation(self):
        ''' Testing the creation of a new group object. '''
        self.assertEqual(self.group.group_name, 'Test Group')
        self.assertEqual(self.group.description, 'Test Description')
        self.assertEqual(self.group.members.count(), 1)

    def test_group_str(self):
        ''' Testing that the string value of a member object is the group.group_name '''
        self.assertEqual(str(self.group), 'Test Group')


class NoteModelTest(TestCase):
    ''' Test cases for Note model. '''
    def setUp(self):
        ''' Setting up data for Note model tests'''
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.member = Member.objects.create(
            user=self.user,
            name='Test Member',
            email='test@testemail.com',
            relationship='Test Relationship'
        )
        self.note = Note.objects.create(
            member=self.member,
            subject='Test Subject',
            content='Test Content'
        )

    def test_note_creation(self):
        ''' Testing the creation of a new Note object. '''
        self.assertEqual(self.note.subject, 'Test Subject')
        self.assertEqual(self.note.content, 'Test Content')

    def test_note_str(self):
        ''' Testing that the string value of a member object is the note.subject '''
        self.assertEqual(str(self.note), 'Test Subject')