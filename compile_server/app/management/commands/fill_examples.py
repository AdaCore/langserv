# The manage.py command to enter examples in the database.
# This is meant to be used by the administrators of the project only.
import glob
import os
from django.core.management.base import BaseCommand

from compile_server.app.models import Resource, Example


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--remove_all', const=True, default=False,
                            action='store_const',
                            help='remove all examples from the database')

        parser.add_argument('--dir', nargs=1, type=str,
                            help='add the example found in the given dir')

    def handle(self, *args, **options):

        if options.get('remove_all', False):
            # Remove all examples from the database
            Resource.objects.all().delete()
            Example.objects.all().delete()

        if options.get('dir', None):
            d = options.get('dir')[0]

            # For now, consider all files in the directory to be part of the
            # example
            if not os.path.isdir(d):
                print "dir parameter should be a directory"
                return

            resources = []
            for file in glob.glob(os.path.join(d, '*')):
                with open(file, 'rB') as f:
                    r = Resource(basename=os.path.basename(file),
                                 contents=f.read())
                    r.save()
                    resources.append(r)

            e = Example(description='hello')
            e.save()
            e.resources.add(*resources)
