import os
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports JOC epub'

    def add_arguments(self, parser):
        parser.add_argument('epub')

    def handle(self, *args, **options):
        epub = options.get('epub')
        if not os.path.exists(epub):
            raise CommandError('epub "%s" does not exist' % epub)
        self.stdout.write(self.style.SUCCESS('Processing "%s"' % epub))
        tree = ET.parse('/home/danny/Dropbox/joc/toc.ncx')
        root = tree.getroot()
        ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
        nav_map_el = root.find('ncx:navMap', ns)
        for chapter in nav_map_el.findall('ncx:navPoint', ns):
            self.stdout.write(self.style.SUCCESS(chapter))
