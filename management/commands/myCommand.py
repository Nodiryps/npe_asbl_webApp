from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'my command ...'

    def add_argument(self, parser):
        pass


    def handle(self, *args, **options):
        try:
            print('Hello world!')
        except Exception as exc:
            CommandError(repr(exc))