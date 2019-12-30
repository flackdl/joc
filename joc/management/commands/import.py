import os
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Imports JOC epub'
    ns: dict

    def add_arguments(self, parser):
        parser.add_argument('epub')

    def handle(self, *args, **options):
        epub = options.get('epub')
        if not os.path.exists(epub):
            raise CommandError('epub "%s" does not exist' % epub)
        self.stdout.write(self.style.SUCCESS('Processing "%s"' % epub))
        tree = ET.parse('/home/danny/Dropbox/joc/toc.ncx')
        root = tree.getroot()
        self.ns = {'ncx': 'http://www.daisy.org/z3986/2005/ncx/'}
        nav_map_el = root.find('ncx:navMap', self.ns)
        for nav_point in nav_map_el.findall('ncx:navPoint', self.ns):
            nav_point_label = nav_point.find('ncx:navLabel', self.ns)
            self.stdout.write(self.style.SUCCESS(nav_point_label[0].text))
            for sub_chapter in self.get_sub_chapters(nav_point, []):
                label = sub_chapter.find('ncx:navLabel', self.ns)
                self.stdout.write(self.style.SUCCESS('\t{}'.format(label[0].text)))

    def get_sub_chapters(self, nav_point: ET.Element, all_sub_nav_points: list):
        sub_chapters = nav_point.find('ncx:navPoint', self.ns)
        if sub_chapters:
            for chapter in sub_chapters:
                print(chapter)
                return self.get_sub_chapters(chapter, all_sub_nav_points)
        return all_sub_nav_points
