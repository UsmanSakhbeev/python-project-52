from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class LabelModelTest(TestCase):
    fixtures = [
        "task_manager/fixtures/test_label.json",
        "task_manager/fixtures/test_user.json",
        "task_manager/fixtures/test_status.json",
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.label = Label.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)

    def test_label_list_view(self):
        response = self.client.get(reverse("label_list"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.get(reverse("label_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_list.html")
        self.assertContains(response, "Label 1")

    def test_create_label(self):
        url = reverse("label_create")
        data = {"name": "Label 3"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Label.objects.filter(name="Label 3").exists())

    def test_update_label(self):
        url = reverse("label_update", args=[self.label.id])
        data = {"name": "Updated label"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertFalse(Label.objects.filter(name="Updated label").exists())

        self.client.force_login(self.user)
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse("label_list"))
        self.assertContains(response, "Label was updated successfully")
        self.label.refresh_from_db()
        self.assertTrue(Label.objects.filter(name="Updated label").exists())

    def test_delete_label(self):
        url = reverse("label_delete", args=[self.label.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name="Label 1").exists())

        self.client.force_login(self.user)
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse("label_list"))
        self.assertContains(response, "Label was deleted successfully")
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_delete_label_with_tasks(self):
        url = reverse("label_delete", args=[self.label.id])
        task = Task.objects.create(
            name="Test Task",
            description="Some description",
            status=self.status,
            author=self.user,
            executor=self.user,
        )
        task.label.add(self.label)
        self.client.force_login(self.user)
        response = self.client.post(url, follow=True)
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        messages = list(response.context["messages"])
        self.assertEqual(
            str(messages[0]),
            "Cannot delete label because it is associated with existing tasks.",
        )
