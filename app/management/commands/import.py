import re
import os
import lxml.html
import xml.etree.ElementTree as ET
from django.contrib.postgres.search import SearchVector
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

        # create search vector for full-text search
        vector = SearchVector('name', weight='A') + SearchVector('instructions', weight='B')
        Recipe.objects.update(search_vector=vector)

    def process_toc_item(self, el: ET.Element, parent=None):
        el_title = el.find('ncx:navLabel/ncx:text', self.ns).text
        children = el.findall('ncx:navPoint', self.ns)
        content = el.find('ncx:content', self.ns)
        # separate content html path and content fragment id
        content_html, content_id = re.match(r'^(.*\.html)(?:#?)(.*)$', content.attrib['src']).groups()
        content_path = os.path.join(self.path, content_html)
        tree = lxml.html.parse(content_path)
        root = tree.getroot()

        # child
        if content_id and not children and parent:
            recipe_el = root.find(".//h3[@id='{}']".format(content_id))
            self.stdout.write(self.style.SUCCESS('Adding recipe {} to {}'.format(recipe_el.text_content(), parent)))
            instruction_el = recipe_el.getnext()
            instructions = []
            # assume every sibling is part of the ingredients until you run hit the end or another recipe
            while True:
                # end of recipe
                if instruction_el is None or instruction_el.tag == 'h3':
                    break
                instructions.append(instruction_el.text_content())
                instruction_el = instruction_el.getnext()
            Recipe.objects.get_or_create(
                name=recipe_el.text_content().lower(),
                defaults=dict(
                    instructions='\n'.join(instructions),
                    category=parent,
                )
            )
        # category
        else:
            self.stdout.write(self.style.SUCCESS('Adding category {}'.format(el_title)))
            category_el = root.find(".//h2")
            descriptions = []
            if category_el is not None:
                category_el = category_el.getnext()
                while True:
                    # end of category
                    if category_el is None or category_el.tag in ['h2', 'h3']:
                        break
                    descriptions.append(category_el.text_content())
                    category_el = category_el.getnext()
            category, was_created = Category.objects.get_or_create(
                name=el_title.lower(),
                defaults=dict(
                    description='\n'.join(descriptions),
                    parent=parent,
                ),
            )
            for child in children:
                self.process_toc_item(child, category)
