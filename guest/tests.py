from django.test import TestCase, Client
from django.urls import reverse
from guest.models import User

class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            contact="1234567890",
            employeid="EMP001",
            email="test@example.com",
            gender="male",
            password="password123"
        )
        self.client = Client()

    def test_login_success(self):
        url = reverse('guest:login')
        response = self.client.post(url, {
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('webuser:home'))
        
    def test_user_home_access_unauthenticated(self):
        url = reverse('webuser:home')
        response = self.client.get(url)
        # Should redirect to login
        self.assertRedirects(response, reverse('guest:login'))

    def test_user_home_access_authenticated(self):
        session = self.client.session
        session['uid'] = self.user.id
        session.save()
        
        url = reverse('webuser:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, Test User")

    def test_edit_profile(self):
        session = self.client.session
        session['uid'] = self.user.id
        session.save()
        
        url = reverse('webuser:editprofile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/Editprofile.html')
        
        # Test POST
        response = self.client.post(url, {
            'name': 'Updated Name',
            'contact': '0987654321',
            'employeid': 'EMP002',
            'email': 'updated@example.com'
        })
        self.assertRedirects(response, reverse('webuser:myprofile'))
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated Name')
        self.assertEqual(self.user.email, 'updated@example.com')
