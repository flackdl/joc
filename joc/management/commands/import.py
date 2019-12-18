import os
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
