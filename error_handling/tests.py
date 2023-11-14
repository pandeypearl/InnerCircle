from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.template import TemplateDoesNotExist

# Create your tests here.
class ErrorHandlingViewsTest(TestCase):
    ''' Unittests for error_handling application views. '''

    def test_custom_400_view(self):
        '''
        Checking that the custom_400 view returns a response with a status code of 400 and uses the 'error_handling/400.html' template.
        '''
        response = self.client.get(reverse('custom_400'))
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'error_handling/400.html')

    def test_custom_401_view(self):
        '''
        Checking that the custom_401 view returns a response with a status code of 401 and uses the 'error_handling/401.html' template.
        '''
        response = self.client.get(reverse('custom_401'))
        self.assertEqual(response.status_code, 401)
        self.assertTemplateUsed(response, 'error_handling/401.html')

    def test_custom_403_view(self):
        '''
        Checking that the custom_403 view returns a response with a status code of 403 and uses the 'error_handling/403.html' template.
        '''
        response = self.client.get(reverse('custom_403'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'error_handling/403.html')

    def test_custom_404_view(self):
        '''
        Checking that the custom_404 view returns a response with a status code of 404 and uses the 'error_handling/404.html' template.
        '''
        response = self.client.get(reverse('custom_404'))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error_handling/404.html')

    def test_custom_405_view(self):
        '''
        Checking that the custom_405 view returns a response with a status code of 405 and uses the 'error_handling/405.html' template.
        '''
        response = self.client.get(reverse('custom_405'))
        self.assertEqual(response.status_code, 405)
        self.assertTemplateUsed(response, 'error_handling/405.html')

    def test_custom_408_view(self):
        '''
        Checking that the custom_408 view returns a response with a status code of 408 and uses the 'error_handling/408.html' template.
        '''
        response = self.client.get(reverse('custom_408'))
        self.assertEqual(response.status_code, 408)
        self.assertTemplateUsed(response, 'error_handling/408.html')

    def test_custom_500_view(self):
        '''
        Checking that the custom_500 view returns a response with a status code of 500 and uses the 'error_handling/500.html' template.
        '''
        response = self.client.get(reverse('custom_500'))
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, 'error_handling/500.html')

    def test_custom_400_view_with_exception(self):
        '''
        Checking that the custom_400 view properly handles an exception message by passing it in the request parameters and rendering it in the template.
        '''
        exception_message = 'Bad Request'
        response = self.client.get(reverse('custom_400'), {'exception': exception_message})
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'error_handling/400.html')
        # Check for content only when the status code is 400
        if response.status_code == 400:
            self.assertContains(response, exception_message, status_code=400)

    def test_custom_403_view_with_exception(self):
        '''
        Checking that the custom_403 view properly handles an exception message by passing it in the request parameters and rendering it in the template.
        '''
        exception_message = 'Forbidden'
        response = self.client.get(reverse('custom_403'), {'exception': exception_message})
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'error_handling/403.html')
        # Checking for content only when the status code is 403
        if response.status_code == 403:
            self.assertContains(response, exception_message, status_code=403)
