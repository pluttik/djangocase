from django.core.management.base import BaseCommand

from cities.views import tick

class Command(BaseCommand):
    """Management command to choose data source and load data for the first time."""
    help = 'Get the data'
    def handle(self, *args, **kwargs):
        global input_type
        input_type = input("Load data via api or csv?")
        self.stdout.write("You chose %s" % input_type)
        tick(input_type)