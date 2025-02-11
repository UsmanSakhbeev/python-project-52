from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskViewTests(TestCase):
    fixtures = [
        "task_manager/fixtures/test_status.json",
        "task_manager/fixtures/test_user.json",
        "task_manager/fixtures/test_task.json",
    ]

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

    def test_task_requires_login(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user1)
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_list.html")
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)

    def test_task_detail_requires_login(self):
        response = self.client.get(reverse("task_detail", args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user1)
        response = self.client.get(reverse("task_detail", args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertContains(response, self.task1.name)

    def test_task_create_requires_login(self):
        response = self.client.post(reverse("task_create"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "New Task",
                "description": "New description",
                "status": 1,
                "executor": self.user2.id,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_requires_login(self):
        response = self.client.post(reverse("task_update", args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("task_update", args=[self.task1.id]),
            {
                "name": "New Task",
                "description": "New description",
                "status": 1,
                "executor": self.user2.id,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_update_forbidden_for_non_author(self) -> None:
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("task_update", args=[self.task1.id]),
            {"name": "Hacked task", "description": "Hacked description"},
            follow=True,
        )
        self.task1.refresh_from_db()
        self.assertNotEqual(self.task1.name, "Hacked task")

    def test_task_delete_requires_login(self):
        response = self.client.get(reverse("task_delete", args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("task_delete", args=[self.task1.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())

    def test_task_delete_forbidden_for_non_author(self):
        self.client.force_login(self.user2)
        response = self.client.post(
            reverse("task_delete", args=[self.task1.id]), follow=True
        )
        self.assertIn(response.status_code, [302, 403])
        self.assertTrue(Task.objects.filter(id=self.task1.id).exists())
