from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


class UserTestCase(TestCase):
    fixtures = ["task_manager/fixtures/test_user.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other_user = User.objects.get(pk=2)
        self.client.force_login(self.user)

    def test_user_list(self):
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ivan")
        self.assertContains(response, "Bradwarden")

    def test_user_create(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "New",
                "last_name": "User",
                "username": "newuser",
                "password1": "securepass123",
                "password2": "securepass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_update(self):
        response = self.client.post(
            reverse("user_update", args=[self.user.pk]),
            {
                "first_name": "UpdatedName",
                "last_name": "UpdatedSurname",
                "username": "Ivannn",
                "password1": "securepass321",
                "password2": "securepass321",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "UpdatedName")

    def test_user_delete(self):
        response = self.client.post(reverse("user_delete", args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="Ivan").exists())
