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
        self.process_categories(root.find('./ncx:navMap', self.ns))

    def process_categories(self, el: ET.Element, parents=None):
        parents = parents or []
        children = el.findall('ncx:navPoint', self.ns)

        # recipe (TODO)
        if not children:
            recipe_name = el.find('ncx:navLabel/ncx:text', self.ns).text
            parent = parents[-1] if parents else None
            print('{}: no children'. format(recipe_name))
            recipe, was_created = Recipe.objects.get_or_create(dict(
                name=recipe_name,
                category=parent,
            ))
            print(recipe, was_created)
        # category
        else:
            for child in children:
                category_title = child.find('ncx:navLabel/ncx:text', self.ns).text
                parent = parents[-1] if parents else None
                category, was_created = Category.objects.get_or_create(dict(
                    name=category_title,
                    parent=parent,
                ))
                self.stdout.write(self.style.SUCCESS('{}{}'.format('\t' * len(parents), category_title)))
                self.process_categories(child, parents + [category])
