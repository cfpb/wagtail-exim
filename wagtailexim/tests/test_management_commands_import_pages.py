import json
import sys
from io import StringIO
from unittest import mock

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from wagtail.core.models import Site, Page
from wagtail.tests.testapp.models import SimplePage


class ImportPagesTests(TestCase):
    def setUp(self):
        self.default_site = Site.objects.get(is_default_site=True)

    def test_import_pages(self):
        self.assertEqual(len(self.default_site.root_page.get_children()), 0)

        mock_data = """
            {
                "pages": [
                    {
                        "app_label": "tests",
                        "model": "simplepage",
                        "data": {
                            "pk": 3,
                            "path": "000100010001",
                            "depth": 3,
                            "numchild": 1,
                            "translation_key": "84799249-a042-4afd-868c-c4a8cffb5cac",
                            "locale": 1,
                            "title": "Test Page",
                            "draft_title": "Test Page",
                            "slug": "test",
                            "content_type": 45,
                            "live": true,
                            "has_unpublished_changes": false,
                            "url_path": "/home/test/",
                            "owner": null,
                            "seo_title": "",
                            "show_in_menus": false,
                            "search_description": "",
                            "go_live_at": null,
                            "expire_at": null,
                            "expired": false,
                            "locked": false,
                            "locked_at": null,
                            "locked_by": null,
                            "first_published_at": null,
                            "last_published_at": null,
                            "latest_revision_created_at": null,
                            "live_revision": null,
                            "alias_of": null,
                            "content": "Testing",
                            "advert_placements": [],
                            "comments": []
                        }
                    },
                    {
                        "app_label": "tests",
                        "model": "simplepage",
                        "data": {
                            "pk": 4,
                            "path": "0001000100010001",
                            "depth": 4,
                            "numchild": 0,
                            "translation_key": "07e05fdc-1d00-46e1-b84f-bd34c25b28c1",
                            "locale": 1,
                            "title": "Test Child Page",
                            "draft_title": "Test Child Page",
                            "slug": "child",
                            "content_type": 45,
                            "live": true,
                            "has_unpublished_changes": false,
                            "url_path": "/home/test/child/",
                            "owner": null,
                            "seo_title": "",
                            "show_in_menus": false,
                            "search_description": "",
                            "go_live_at": null,
                            "expire_at": null,
                            "expired": false,
                            "locked": false,
                            "locked_at": null,
                            "locked_by": null,
                            "first_published_at": null,
                            "last_published_at": null,
                            "latest_revision_created_at": null,
                            "live_revision": null,
                            "alias_of": null,
                            "content": "Testing content",
                            "advert_placements": [],
                            "comments": []
                        }
                    }
                ]
            }
        """

        with mock.patch("builtins.open", mock.mock_open(read_data=mock_data)) as mock_file:
            call_command('import_pages', 'testfile.json')

        self.default_site.root_page.refresh_from_db()

        self.assertEqual(len(self.default_site.root_page.get_children()), 1)

        children = self.default_site.root_page.get_children()
        self.assertEqual(len(children), 1)
        self.assertEqual(children.first().title, "Test Page")
        self.assertEqual(children.first().url_path, "/home/test/")
