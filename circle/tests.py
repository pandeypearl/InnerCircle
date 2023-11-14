''' Unit tests for the circle application. '''
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
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


class CircleViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create some test data for groups and members
        self.group = Group.objects.create(user=self.user, group_name='Test Group', description='Test Description')
        self.member = Member.objects.create(user=self.user, name='Test Member', email='test@example.com')

    def test_group_list_view(self):
        '''
        Testing that the group_list view returns a status code of 200 and uses the correct template.
        '''
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('group_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'circle/group_list.html')

    def test_group_detail_view(self):
        '''
        Testing that the group_detail view returns a status code of 200 and uses the correct template.
        '''
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('group_detail', args=[self.group.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'circle/group_detail.html')

    def test_create_group_view(self):
        '''
        Testing that the create_group view creates a new group and redirects to the group_list view.
        '''
        self.client.login(username='testuser', password='testpass')
        data = {'group_name': 'New Group', 'description': 'New Description'}
        response = self.client.post(reverse('create_group'), data)
        self.assertEqual(response.status_code, 302)  # 302 indicates a successful redirect
        self.assertRedirects(response, reverse('group_list'))

    def test_edit_group_view(self):
        '''
        Testing that the edit_group view updates an existing group and redirects to the group_list view.
        '''
        self.client.login(username='testuser', password='testpass')
        data = {'group_name': 'Updated Group', 'description': 'Updated Description'}
        response = self.client.post(reverse('edit_group', args=[self.group.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('group_list'))

    def test_delete_group_view(self):
        '''
        Testing that the delete_group view deletes an existing group and redirects to the group_list view.
        '''
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_group', args=[self.group.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('group_list'))

    def test_member_list_view(self):
        '''
        Testing that the member_list view returns a status code of 200 and uses the correct template.
        '''
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('member_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'circle/member_list.html')

    def test_member_detail_view(self):
        '''
        Testing that the member_detail view returns a status code of 200 and uses the correct template.
        '''
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('member_detail', args=[self.member.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'circle/member_detail.html')

    def test_create_member_view(self):
        '''
        Testing that the create_member view creates a new member and redirects to the member_list view.
        '''
        self.client.login(username='testuser', password='testpass')
        data = {'name': 'New Member', 'email': 'new@example.com'}
        response = self.client.post(reverse('create_member'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('member_list'))

    def test_edit_member_view(self):
        '''
        Testing that the edit_member view updates an existing member and redirects to the member_list view.
        '''
        self.client.login(username='testuser', password='testpass')
        data = {'name': 'Updated Member', 'email': 'updated@example.com'}
        response = self.client.post(reverse('edit_member', args=[self.member.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('member_list'))

    def test_delete_member_view(self):
        '''
        Testing that the delete_member view deletes an existing member and redirects to the member_list view.
        '''
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('delete_member', args=[self.member.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('member_list'))
