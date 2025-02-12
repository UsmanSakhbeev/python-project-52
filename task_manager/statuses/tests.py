from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class StatusModelTest(TestCase):
    fixtures = ["task_manager/fixtures/test_user.json"]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.status1 = Status.objects.create(name="In progress")
        self.status2 = Status.objects.create(name="Finished")

    def test_name_label(self):
        field_label = self.status1._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    def test_status_list_view(self):
        response = self.client.get(reverse("status_list"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.get(reverse("status_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/status_list.html")
        self.assertContains(response, "In progress")
        self.assertContains(response, "Finished")

    def test_create_status(self):
        url = reverse("status_create")
        data = {"name": "Completed"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name="Completed").exists())

        self.client.force_login(self.user)
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse("status_list"))
        self.assertContains(response, "Status was created successfully")

        self.assertTrue(Status.objects.filter(name="Completed").exists())

    def test_update_status(self):
        url = reverse("status_update", args=[self.status1.id])
        data = {"name": "Updated_name"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.status1.refresh_from_db()
        self.assertNotEqual(self.status1.name, "Updated_name")

        self.client.force_login(self.user)
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse("status_list"))
        self.assertContains(response, "Status was updated successfully")

        self.status1.refresh_from_db()
        self.assertEqual(self.status1.name, "Updated_name")

    def test_delete_status(self):
        url = reverse("status_delete", args=[self.status1.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(id=self.status1.id).exists())

        self.client.force_login(self.user)
        response = self.client.post(url, follow=True)
        self.assertRedirects(response, reverse("status_list"))
        self.assertContains(response, "Status was deleted successfully")

        self.assertFalse(Status.objects.filter(id=self.status1.id).exists())

    def test_delete_status_with_tasks(self):
        url = reverse("status_delete", args=[self.status1.id])
        Task.objects.create(
            name="Test Task",
            description="Some description",
            status=self.status1,
            author=self.user,
            executor=self.user,
        )

        self.client.force_login(self.user)
        response = self.client.post(url, follow=True)
        self.assertTrue(Status.objects.filter(id=self.status1.id).exists())
        messages = list(response.context["messages"])
        self.assertEqual(
            str(messages[0]),
            "Cannot delete status because it is associated with existing tasks.",
        )
