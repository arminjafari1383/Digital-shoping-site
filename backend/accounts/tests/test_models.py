from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):

        user = User.objects.create_user(
            email="test@example.com",
            password = "12345678"
        )

        self.assertEqual(
            user.email,
            "test@example.com"
        )

        self.assertTrue(
            user.check_password("1245678")
        )


    def test_create_superuser(self):

        admin = User.objects.create_superuser(
            email="arminjafri138386@gmail.com",
            password="a"
        )

        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

