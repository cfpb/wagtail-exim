import argparse
import json
import sys

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.http.response import Http404

from wagtail.core.models import Site, Page


class Command(BaseCommand):

    def add_arguments(self, parser):
        # parser.add_argument("--site")
        parser.add_argument(
            "input",
            type=argparse.FileType("r"),
            default=sys.stdin,
            help="Specifies the file with page data to import"
        )

    def handle(self, *args, **options):
        input_file = options["input"]
        import_data = json.load(input_file)

        site = Site.objects.get(is_default_site=True)
        for page_data in import_data["pages"]:
            path_components = [
                component
                for component in page_data["data"]["url_path"].split("/")
                if component
            ]
            page_url = "/".join(path_components[1:])

            try:
                parent_route = site.root_page.route(
                    None,
                    # Drop the site root slug and the page"s slug from the
                    # path_components to resolve the parent page
                    path_components[1:-1]
                )
            except Http404:
                raise CommandError(
                    f"Couldn't find parent for page at {page_url}"
                )

            # Construct a bare Page object first to get the treebeard
            # assignments right.
            page = Page.from_serializable_data(page_data["data"])

            # These will all be set appropriate when we call add_child
            page.pk = None
            page.path = None
            page.depth = None
            page.numchild = 0
            page.url_path = None

            # Add the page to the parent
            parent_route.page.add_child(instance=page)

            # Now set up the specific Page
            model = apps.get_model(page_data["app_label"], page_data["model"])
            specific_page = model.from_serializable_data(page_data["data"])
            specific_page.__dict__.update(page.__dict__)
            specific_page.page_ptr = page
            specific_page.save()

            self.stdout.write(f"Created page {page_url}")
