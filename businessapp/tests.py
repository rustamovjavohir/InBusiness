import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import resolve, reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework_simplejwt.models import TokenUser
from rest_framework.authtoken.models import Token

# Create your tests here.
from auth_user.models import User


class TestProject(APITestCase):

    def setUp(self):
        image = io.BytesIO()
        Image.new('RGB', (400, 200)).save(image, 'JPEG')
        image.seek(0)
        image_file = SimpleUploadedFile('image.jpg', image.getvalue())

        self.image = image
        self.create_url = reverse('project_create')
        self.list_url = reverse('project_list')
        self.user_data = {
            "first_name": 'Javohir',
            "last_name": 'Rustamov',
            "password": 'password',
            "username": 'user1',
            "email": 'user1@gmail.com',
            "data_of_birth": '2000-05-27',
            "is_staff": True,
        }
        self.create_data = {
            "title": "title1",
            "image": image_file,
            "description": "description1",
            "cost_investments": 2500.0,
            "is_active": True,
            "age_business": 5,
            "number_employees": 10,
            "organizational_type": "OOO",
            "is_delete": False,
            "created_by": 1,

        }

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
