from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from accounts.models import User


class Command(BaseCommand):
    help = 'my command ...'


    def handle(self, *args, **options):
    #    try:
    #       sendMailToSponsors()
        send_mail(
            'Rappel mensualité parrainage',
            f'Bonjour Spyridon,\nCeci est le mail pour les marraines.\n\nBisous!',
            'npe.asbl@gmail.com',
            ['spyridon.theodorou@hotmail.com'],
            fail_silently = False,
        )
    #    except Exception as exc:
    #        CommandError(repr(exc))



