"""Tests for app.interface.contact_flows."""

import contextlib
import io
import unittest
from unittest import mock

from app.configs.settings import NOT_PROVIDED
from app.interface import contact_flows as flows

ANA = {"id": 1, "name": "Ana", "phone": "111", "email": "ana@example.com"}
LUIS = {"id": 2, "name": "Luis", "phone": "222", "email": "luis@example.com"}


class FlowTestCase(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.object(flows, "save_contacts")
        self.save = patcher.start()
        self.addCleanup(patcher.stop)

    def run_flow(self, flow, contacts, inputs=()):
        """Runs a flow with scripted answers and returns its result and output."""
        output = io.StringIO()
        with mock.patch("builtins.input", side_effect=list(inputs)):
            with contextlib.redirect_stdout(output):
                result = flow(contacts)
        return result, output.getvalue()


class AddContactFlowTests(FlowTestCase):
    def test_adds_saves_and_reports_success(self):
        result, output = self.run_flow(
            flows.add_contact_flow, [], ["Eva", "55", "eva@example.com"]
        )

        self.assertEqual(result[0]["name"], "Eva")
        self.save.assert_called_once_with(result)
        self.assertIn("added successfully", output)

    def test_empty_name_returns_to_menu(self):
        result, output = self.run_flow(flows.add_contact_flow, [ANA], [""])

        self.assertEqual(result, [ANA])
        self.save.assert_not_called()
        self.assertIn("Name cannot be empty", output)

    def test_invalid_phone_and_email_are_asked_again(self):
        result, output = self.run_flow(
            flows.add_contact_flow, [], ["Eva", "abc", "55", "bad", "eva@example.com"]
        )

        self.assertEqual(result[0]["phone"], "55")
        self.assertEqual(result[0]["email"], "eva@example.com")
        self.assertIn("digits only", output)
        self.assertIn("Email must have", output)

    def test_failed_save_keeps_old_list_and_never_reports_success(self):
        self.save.side_effect = PermissionError("denied")

        result, output = self.run_flow(flows.add_contact_flow, [ANA], ["Eva", "", ""])

        self.assertEqual(result, [ANA])
        self.assertIn("Could not save", output)
        self.assertNotIn("added successfully", output)

    def test_duplicate_declined_does_not_save(self):
        result, output = self.run_flow(
            flows.add_contact_flow, [ANA], ["Eva", "111", "", "no"]
        )

        self.assertEqual(result, [ANA])
        self.save.assert_not_called()
        self.assertIn("already used", output)

    def test_duplicate_accepted_saves(self):
        result, _ = self.run_flow(
            flows.add_contact_flow, [ANA], ["Eva", "111", "", "yes"]
        )
        self.assertEqual(len(result), 2)


class ReadFlowTests(FlowTestCase):
    def test_view_all_lists_contacts(self):
        _, output = self.run_flow(flows.view_all_contacts_flow, [ANA])
        self.assertIn("[1] Ana", output)

    def test_view_all_empty(self):
        _, output = self.run_flow(flows.view_all_contacts_flow, [])
        self.assertIn("No contacts found", output)

    def test_search_shows_only_matches(self):
        _, output = self.run_flow(flows.search_contacts_flow, [ANA, LUIS], ["lui"])
        self.assertIn("Luis", output)
        self.assertNotIn("Ana", output)

    def test_search_without_matches(self):
        _, output = self.run_flow(flows.search_contacts_flow, [ANA], ["zzz"])
        self.assertIn("No contacts match 'zzz'", output)

    def test_search_rejects_empty_text(self):
        _, output = self.run_flow(flows.search_contacts_flow, [ANA], [""])
        self.assertIn("Search text cannot be empty", output)


class UpdateContactFlowTests(FlowTestCase):
    def test_changes_only_entered_fields(self):
        result, output = self.run_flow(
            flows.update_contact_flow, [ANA], ["1", "Ana G", "", ""]
        )

        self.assertEqual(result[0], {**ANA, "name": "Ana G"})
        self.save.assert_called_once()
        self.assertIn("updated successfully", output)

    def test_dash_clears_optional_fields(self):
        result, _ = self.run_flow(flows.update_contact_flow, [ANA], ["1", "", "-", "-"])
        self.assertEqual(result[0]["phone"], NOT_PROVIDED)
        self.assertEqual(result[0]["email"], NOT_PROVIDED)

    def test_blank_answers_do_not_save(self):
        result, output = self.run_flow(
            flows.update_contact_flow, [ANA], ["1", "", "", ""]
        )

        self.assertEqual(result, [ANA])
        self.save.assert_not_called()
        self.assertIn("No changes made", output)

    def test_invalid_id_is_asked_again(self):
        _, output = self.run_flow(
            flows.update_contact_flow, [ANA], ["1_0", "abc", "1", "", "", ""]
        )
        self.assertEqual(output.count("positive whole number"), 2)

    def test_unknown_id(self):
        _, output = self.run_flow(flows.update_contact_flow, [ANA], ["9"])
        self.assertIn("ID 9 not found", output)

    def test_own_phone_is_not_a_duplicate(self):
        result, output = self.run_flow(
            flows.update_contact_flow, [ANA], ["1", "", "111", ""]
        )
        self.assertNotIn("already used", output)
        self.assertEqual(result, [ANA])

    def test_duplicate_declined_does_not_save(self):
        result, _ = self.run_flow(
            flows.update_contact_flow, [ANA, LUIS], ["1", "", "222", "", "no"]
        )
        self.assertEqual(result, [ANA, LUIS])
        self.save.assert_not_called()

    def test_failed_save_keeps_old_values(self):
        self.save.side_effect = OSError("disk full")

        result, output = self.run_flow(
            flows.update_contact_flow, [ANA], ["1", "New", "", ""]
        )

        self.assertEqual(result, [ANA])
        self.assertNotIn("updated successfully", output)


class DeleteContactFlowTests(FlowTestCase):
    def test_confirmed(self):
        result, output = self.run_flow(flows.delete_contact_flow, [ANA], ["1", "Y"])

        self.assertEqual(result, [])
        self.save.assert_called_once_with([])
        self.assertIn("'Ana' deleted", output)

    def test_cancelled(self):
        result, output = self.run_flow(flows.delete_contact_flow, [ANA], ["1", "no"])

        self.assertEqual(result, [ANA])
        self.save.assert_not_called()
        self.assertIn("Deletion cancelled", output)

    def test_failed_save_keeps_contact(self):
        self.save.side_effect = PermissionError("denied")

        result, output = self.run_flow(flows.delete_contact_flow, [ANA], ["1", "yes"])

        self.assertEqual(result, [ANA])
        self.assertNotIn("deleted.", output)


class ExportContactsFlowTests(FlowTestCase):
    def test_reports_exported_path(self):
        with mock.patch.object(
            flows, "export_contacts_csv", return_value="out.csv"
        ) as export:
            result, output = self.run_flow(flows.export_contacts_flow, [ANA])

        export.assert_called_once_with([ANA])
        self.assertEqual(result, [ANA])
        self.assertIn("1 contact(s) exported to out.csv", output)

    def test_reports_failure(self):
        with mock.patch.object(
            flows, "export_contacts_csv", side_effect=PermissionError("in use")
        ):
            _, output = self.run_flow(flows.export_contacts_flow, [ANA])

        self.assertIn("Could not export", output)

    def test_empty_list(self):
        _, output = self.run_flow(flows.export_contacts_flow, [])
        self.assertIn("No contacts available", output)


if __name__ == "__main__":
    unittest.main()
