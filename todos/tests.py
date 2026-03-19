from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(
    VM_CONTROL_COMMANDS={
        "vm1": {
            "name": "Virtual Machine 1",
            "power_on": ["echo", "vm1-on"],
            "power_off": ["echo", "vm1-off"],
        }
    }
)
class VmControlTests(TestCase):
    def test_index_page_shows_vm_name(self):
        response = self.client.get(reverse("todos:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VM Power Control")
        self.assertContains(response, "Virtual Machine 1")

    @patch("todos.views.subprocess.run")
    def test_power_on_posts_command(self, mocked_run):
        response = self.client.post(
            reverse("todos:control_vm", kwargs={"vm_id": "vm1"}),
            {"action": "power_on"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        mocked_run.assert_called_once()
        command = mocked_run.call_args[0][0]
        self.assertEqual(command, ["echo", "vm1-on"])

    def test_invalid_action_sets_error(self):
        response = self.client.post(
            reverse("todos:control_vm", kwargs={"vm_id": "vm1"}),
            {"action": "invalid"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        messages = [str(message) for message in response.context["messages"]]
        self.assertIn("Invalid VM action.", messages)
