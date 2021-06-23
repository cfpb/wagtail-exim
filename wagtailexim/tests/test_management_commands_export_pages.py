import json
from io import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from wagtail.core.models import Site, Page
from wagtail.tests.testapp.models import SimplePage


class ExportPagesTests(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)

        self.test_page = SimplePage(
            title="Test Page",
            slug="test",
            content="Testing",
        )
        self.default_site.root_page.add_child(instance=self.test_page)
        self.test_page.save()

        self.child_page = SimplePage(
            title="Test Child Page",
            slug="child",
            content="Testing content",
        )
        self.test_page.add_child(instance=self.child_page)
        self.child_page.save()

    def test_export_pages(self):
        out = StringIO()
        call_command('export_pages', "/test/", output=out)
        data = json.loads(out.getvalue())

        self.assertEqual(len(data["pages"]), 1)

        self.assertEqual(data["pages"][0]["app_label"], "tests")
        self.assertEqual(data["pages"][0]["model"], "simplepage")
        self.assertEqual(data["pages"][0]["data"]["title"], "Test Page")
        self.assertEqual(data["pages"][0]["data"]["url_path"], "/home/test/")

    def test_export_pages_not_found(self):
        with self.assertRaises(CommandError):
            call_command('export_pages', "test-not-found")

    def test_export_pages_ancestors(self):
        out = StringIO()
        call_command(
            'export_pages',
            "/test/child/",
            include_ancestors=True,
            output=out
        )
        data = json.loads(out.getvalue())

        # There should be two pages in the export and the requested bage should
        # be last
        self.assertEqual(len(data["pages"]), 2)
        self.assertEqual(data["pages"][0]["data"]["url_path"], "/home/test/")
        self.assertEqual(
            data["pages"][1]["data"]["url_path"], "/home/test/child/"
        )

    def test_export_pages_descendants(self):
        out = StringIO()
        call_command(
            'export_pages',
            "/test/",
            include_descendants=True,
            output=out
        )
        data = json.loads(out.getvalue())

        # There should be two pages in the export and the requested bage should
        # be last
        self.assertEqual(len(data["pages"]), 2)
        self.assertEqual(data["pages"][0]["data"]["url_path"], "/home/test/")
        self.assertEqual(
            data["pages"][1]["data"]["url_path"], "/home/test/child/"
        )


