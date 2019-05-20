import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .forms import RegistrationForm, ProductForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Product, Dish, SportActivity, TipStudy, SportActivityNotification
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ObjectDoesNotExist
from .forms import TodoForm
from .models import Todo


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


class ProductAdminTest(TestCase):

    def setUp(self):
        self.product1 = Product.objects.create(
            name_product='test',
            description='test description',
            price=25
        )
        self.site = AdminSite()

    def test_add(self):
        self.assertEqual(self.product1.id, 1)

    def test_delete(self):
        product2 = Product.objects.create(
            name_product='test',
            description='test description',
            price=25
        )
        product3 = Product.objects.create(
            name_product='test',
            description='test description',
            price=25
        )
        Product.objects.get(id=2).delete()
        with self.assertRaises(ObjectDoesNotExist):
            Product.objects.get(id=2)

    def test_changefields(self):
        product = Product.objects.create(
            name_product='test',
            description='test description',
            price=25
        )
        product_change = Product.objects.create(
            name_product='change',
            description='test description',
            price=25
        )
        form = ProductForm(instance=product)
        form.fields['name_product'] = 'change'
        if form.is_valid():
            form.save()
        self.assertEqual('change', form.fields['name_product'])


class DishAdminTest(TestCase):

    def setUp(self):
        self.dish1 = Dish.objects.create(
            name='test',
            description='test description',
        )
        self.site = AdminSite()

    def test_add(self):
        self.assertEqual(self.dish1.id, 1)

    def test_changefields(self):
        dish = Dish.objects.create(
            name='test',
            description='test description',
        )
        dish_change = Dish.objects.create(
            name='change',
            description='test description',
        )
        form = ProductForm(instance=dish)
        form.fields['name'] = 'change'
        if form.is_valid():
            form.save()
        self.assertEqual('change', form.fields['name'])

    def test_delete(self):
        dish2 = Dish.objects.create(
            name='test',
            description='test description',
        )
        dish3 = Dish.objects.create(
            name='test',
            description='test description',
        )
        Dish.objects.get(id=2).delete()
        with self.assertRaises(ObjectDoesNotExist):
            Dish.objects.get(id=2)


class SportAdminTest(TestCase):

    def setUp(self):
        self.sport1 = SportActivity.objects.create(
            activity_name='test',
            description='test description',
            time=datetime.timedelta(days=20, hours=10),
        )
        self.site = AdminSite()

    def test_add(self):
        self.assertEqual(self.sport1.id, 1)

    def test_delete(self):
        sport2 = SportActivity.objects.create(
            activity_name='test',
            description='test description',
            time=datetime.timedelta(days=20, hours=10)
        )
        sport3 = SportActivity.objects.create(
            activity_name='test',
            description='test description',
            time=datetime.timedelta(days=20, hours=10)
        )
        SportActivity.objects.get(id=2).delete()
        with self.assertRaises(ObjectDoesNotExist):
            SportActivity.objects.get(id=2)

    def test_changefields(self):
        sport = SportActivity.objects.create(
            activity_name='test',
            description='test description',
            time=datetime.timedelta(days=20, hours=10)
        )
        sport_change = SportActivity.objects.create(
            activity_name='change',
            description='test description',
            time=datetime.timedelta(days=20, hours=10)
        )
        form = ProductForm(instance=sport)
        form.fields['activity_name'] = 'change'
        if form.is_valid():
            form.save()
        self.assertEqual('change', form.fields['activity_name'])


class StudyTipAdminTest(TestCase):
    def setUp(self):
        self.study1 = TipStudy.objects.create(
            tip='test',
            description='test description',
        )
        self.site = AdminSite()

    def test_changefields(self):
        study = TipStudy.objects.create(
            tip='test',
            description='test description',
        )
        study_change = TipStudy.objects.create(
            tip='change',
            description='test description',
        )
        form = ProductForm(instance=study)
        form.fields['tip'] = 'change'
        if form.is_valid():
            form.save()
        self.assertEqual('change', form.fields['tip'])

    def test_add(self):
        self.assertEqual(self.study1.id, 1)

    def test_delete(self):
        study2 = TipStudy.objects.create(
            tip='test',
            description='test description',
        )
        study3 = TipStudy.objects.create(
            tip='test',
            description='test description',
        )
        TipStudy.objects.get(id=2).delete()
        with self.assertRaises(ObjectDoesNotExist):
            TipStudy.objects.get(id=2)


class DeleteUserTest(TestCase):

    def setUp(self):
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

    def test_delete(self):
        User.objects.get(id=1).delete()
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=1)


class SportActivityNotfication(TestCase):

    def setUp(self):
        userc = User.objects.create_user(username='testuser', password='A123456b')
        SportActivity.objects.create(activity_name='Football',
                                                      description='This is Test',
                                                      time=datetime.timedelta(minutes=40))

        SportActivityNotification.objects.create(activity_name='Football', link=userc)

    def test_link(self):
        self.assertEqual('testuser', User.objects.get(username='testuser').username)

    def test_activity(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(SportActivityNotification.objects.get(activity_name='Football', link=user).activity_name,
                         SportActivity.objects.get(activity_name='Football').activity_name)


class TodoTest(TestCase):
    def setUp(self):
        userc = User.objects.create_user(username='testuser', password='A123456b')
        self.client.login(username='testuser', password='A123456b')
        Todo.objects.create(text="test todo", user=User.objects.get(username='testuser'))

    def test_form_valid(self):
        form_data = {'text': 'This is a todo test'}
        form = TodoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add(self):
        response = self.client.post("/todo/", {'text': 'test todo'})
        self.assertEqual(response.status_code, 200)
        print(response)
        self.assertEqual(Todo.objects.get(text='test todo', user=User.objects.get(username='testuser')).text, 'test todo')






