import argparse
import json
import sys

from django.core.management.base import BaseCommand, CommandError
from django.http.response import Http404
from django.core.serializers.json import DjangoJSONEncoder

from wagtail.core.models import Site, Page


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            "pages", metavar="PAGE", nargs="+",
            help="URL path to the page to export"
        )

        # parser.add_argument("--include-children")
        parser.add_argument(
            '--include-ancestors',
            action='store_true',
            help=(
                "Include ancestors , up to but not including the site root, "
                "in the export."
            ),
        )
        parser.add_argument(
            '--include-descendants',
            action='store_true',
            help="Include descendants in the export.",
        )

        parser.add_argument(
            "-o", "--output", type=argparse.FileType("w"), default=sys.stdout,
            help="Specifies file to which the output is written."
        )

    def handle(self, *args, **options):
        output = options["output"]
        data = {
            "pages": []
        }

        site = Site.objects.get(is_default_site=True)
        root_ancestors = site.root_page.get_ancestors(inclusive=True)
        for page_path in options["pages"]:
            path_components = [
                component for component in page_path.split("/") if component
            ]
            try:
                route = site.root_page.route(None, path_components)
            except Http404:
                raise CommandError(
                    f"Couldn't find page matching {page_path}"
                )

            if options['include_ancestors']:
                ancestors = route.page.get_ancestors().exclude(
                    pk__in=root_ancestors
                )
                for ancestor in ancestors:
                    data["pages"].append(self.export_page(ancestor.specific))

            data["pages"].append(self.export_page(route.page))

            if options['include_descendants']:
                descendants = route.page.get_descendants()
                for descendant in descendants:
                    data["pages"].append(self.export_page(descendant.specific))

        json.dump(
            data,
            output,
            ensure_ascii=False,
            indent=4,
            cls=DjangoJSONEncoder
        )

    def export_page(self, page):
        return {
            "app_label": page.content_type.app_label,
            "model": page.content_type.model,
            "data": page.serializable_data(),
        }
