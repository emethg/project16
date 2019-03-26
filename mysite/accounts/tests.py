from django.test import TestCase, Client
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib.auth.forms import PasswordChangeForm


# Create your tests here.


class RegistrationFormTests(TestCase):

    def test_registration_form_valid(self):
        data = {'username': 'emeth',
                'password1': 'E123456g',
                'password2': 'E123456g',
                'email': 'emeth@gmail.com'
                }
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.username, "emeth")
        self.assertEqual(comment.email, "emeth@gmail.com")

    def test_registration_form_invalid(self):
        data = {'username': 'emeth',
                'password1': 'emeth',
                'password2': 'emeth',
                'email': 'emeth@gmail.com'
                }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())

        data = {'username': 'emeth',
                'password1': 'E12345g',
                'password2': 'E12345g',
                'email': 'emeth@gmail.com'
                }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())

        data = {'username': 'emeth',
                'password1': 'E12345',
                'password2': 'E12345g',
                'email': 'emeth@gmail.com'
                }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())

        data = {'username': 'emeth',
                'password1': 'E12345g',
                'password2': 'E12345g',
                }
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())

        form = RegistrationForm({})
        self.assertFalse(form.is_valid())


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)


class ChangePasswordTest(TestCase):

    def setUp(self):
        self.data = {'username': 'yaniv',
                'password1': 'Y123456b',
                'password2': 'Y123456b',
                'email': 'yaniv@gmail.com'
                }
        form = RegistrationForm(self.data)
        self.assertTrue(form.is_valid())
        form.save()
        self.client.post('/login/', self.data, follow=True)

    def test_change_succeed(self):
        user = User.objects.get(username='yaniv')
        data = {
            'old_password': 'Y123456b',
            'new_password1': 'E123456g',
            'new_password2': 'E123456g',
        }
        form = PasswordChangeForm(user, data)
        self.assertTrue(form.is_valid())

    def test_change_no_succeed(self):
        user = User.objects.get(username='yaniv')
        data = {
            'old_password': 'Y123456b',
            'new_password1': 'E123456g',
            'new_password2': 'E123456g',
        }
        form = PasswordChangeForm(user, data)
        self.assertTrue(form.is_valid())

class LogoutTest(TestCase):

    def test_logout(self):
        self.client = Client()
        self.client.login(username='emeth', password='E123456g')
        response1 = self.client.get('/profile', follow=True)
        self.client.logout()
        response2 = self.client.get('/profile', follow=True)
        self.assertNotEqual(response1, response2)
