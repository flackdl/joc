import re
import os
import lxml.html
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError

from app.models import Category, Recipe


class Command(BaseCommand):
    help = 'Imports JOC epub'
    ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
    path: str = None

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, *args, **options):
        self.path = options.get('path')
        if not os.path.exists(self.path):
            raise CommandError('path "%s" does not exist' % self.path)
        self.stdout.write(self.style.SUCCESS('Processing "%s"' % self.path))
        tree = ET.parse(os.path.join(self.path, 'toc.ncx'))
        root = tree.getroot()
        for nav_point in root.findall('./ncx:navMap/ncx:navPoint', self.ns):
            self.process_toc_item(nav_point)

    def process_toc_item(self, el: ET.Element, parent=None):
        el_title = el.find('ncx:navLabel/ncx:text', self.ns).text
        children = el.findall('ncx:navPoint', self.ns)

        # child
        if not children and parent:
            content = el.find('ncx:content', self.ns)
            content_html = re.sub(r'#.*', '', content.attrib['src'])  # remove fragment
            content_path = os.path.join(self.path, content_html)
            tree = lxml.html.parse(content_path)
            root = tree.getroot()
            for recipe in root.findall('.//h3'):
                self.stdout.write(self.style.SUCCESS('Adding recipe {} to {}'.format(recipe.text_content(), parent)))
                instructions = []
                instruction_el = recipe.getnext()
                while True:
                    if instruction_el is None:
                        break
                    instructions.append(instruction_el.text_content())
                    instruction_el = instruction_el.getnext()
                Recipe.objects.get_or_create(
                    name=recipe.text_content(),
                    defaults=dict(
                        instructions='\n'.join(instructions),
                        category=parent,
                    )
                )
        # category
        else:
            self.stdout.write(self.style.SUCCESS('Adding category {}'.format(el_title)))
            category, was_created = Category.objects.get_or_create(
                name=el_title,
                defaults=dict(
                    parent=parent,
                ),
            )
            for child in children:
                self.process_toc_item(child, category)
