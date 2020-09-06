from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from accounts.models import User


class Command(BaseCommand):
    help = 'my command ...'

    EMAIL_ADDRESS_NPE = 'npe.asbl@gmail.com'
    MSG_SPONSORS = """
        \nJuste pour être sûr que tu n'oublieras pas le.s loulou.s que tu parraines (ça arrive aux meilleur.e.s, ne t'inquiètes pas :D ).
        \nPour faciliter tout cela, tu peux aussi faire une domiciliation. C'est comme tu préfères :).
        \nL'équipe Nous Pour Eux a.s.b.l. te souhaite une agréable journée et te remercie encore pour ton implication et tes dons!
        \nMERCI!! :)
        \n\nNous Pour Eux a.s.b.l.
    """


    def sendMailToSponsors(self):
    #    sponsors = User.objects.filter(isSponsor=True)
    #    for user in sponsors:
        send_mail(
            'Rappel mensualité parrainage',
            f'Bonjour Spyridon,\n{self.MSG_SPONSORS}',
            self.EMAIL_ADDRESS_NPE,
            ['spyridon.theodorou@hotmail.com'],
            fail_silently = False,
        )


#    def sendMailToAdmin():



    def add_argument(self, parser):
        pass


    def handle(self, *args, **options):
        try:
            self.sendMailToSponsors()
        except Exception as exc:
            CommandError(repr(exc))