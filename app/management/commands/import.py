import os
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError

from app.models import Category, Recipe


class Command(BaseCommand):
    help = 'Imports JOC epub'
    ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}

    def add_arguments(self, parser):
        parser.add_argument('epub')

    def handle(self, *args, **options):
        epub = options.get('epub')
        if not os.path.exists(epub):
            raise CommandError('epub "%s" does not exist' % epub)
        self.stdout.write(self.style.SUCCESS('Processing "%s"' % epub))
        tree = ET.parse('/home/danny/Dropbox/joc/toc.ncx')
        root = tree.getroot()
        for nav_point in root.findall('./ncx:navMap/ncx:navPoint', self.ns):
            self.process_categories(nav_point)

    def process_categories(self, el: ET.Element, parent=None):
        el_title = el.find('ncx:navLabel/ncx:text', self.ns).text
        children = el.findall('ncx:navPoint', self.ns)
        self.stdout.write(self.style.SUCCESS('Processing {}'.format(el_title)))

        # recipe (TODO)
        if not children:
            recipe_name = el.find('ncx:navLabel/ncx:text', self.ns).text
            print('{}: no children for cat: {}'. format(recipe_name, parent))
            if parent:
                Recipe.objects.get_or_create(
                    name=recipe_name,
                    category=parent,
                )
        # category
        else:
            print('Creating {} for {}'.format(el_title, parent))
            category, was_created = Category.objects.get_or_create(
                name=el_title,
                parent=parent,
            )
            for child in children:
                self.process_categories(child, category)
