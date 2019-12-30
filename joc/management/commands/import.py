import os
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError


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
        self.process_chapters(root.find('./ncx:navMap', self.ns))

    def process_chapters(self, el: ET.Element, parents=None):
        parents = parents or []
        children = el.findall('ncx:navPoint', self.ns)
        for child in children:
            chapter = child.find('ncx:navLabel/ncx:text', self.ns).text
            self.stdout.write(self.style.SUCCESS('{}{}'.format('\t' * len(parents), chapter)))
            self.process_chapters(child, parents + [chapter])
