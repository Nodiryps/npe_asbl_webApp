from django.core.management.base import BaseCommand
from django.core.mail import send_mail
import datetime
import sys


class Command(BaseCommand):
    help = 'my command ...'

    EMAIL_SUBJECT    = 'Liste des chiens: suivi mensuel'
    EMAIL_BODY       = '\n\nC\'est un mail test :)\n\nXOXO'
    EMAIL_SENDER     = 'npe.asbl@gmail.com'
    EMAIL_RECIPIENTS = ['spyridon.theodorou@hotmail.com']


    def handle(self, *args, **options):
        if datetime.datetime.today().day != 18:
            sys.exit(0)

        send_mail(
            self.EMAIL_SUBJECT,
            f'Bonjour Spyridon,{self.EMAIL_BODY}',
            self.EMAIL_SENDER,
            self.EMAIL_RECIPIENTS,
            fail_silently = False,
        )



