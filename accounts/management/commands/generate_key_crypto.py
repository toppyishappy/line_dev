from django.core.management.base import BaseCommand
from utils.crypto import CryptoGraphy
# from core.models import ScopeProject

class Command(BaseCommand):
    help = 'Init Gentrate Key Crypto'

    def handle(self, *args, **options):
        obj = CryptoGraphy()
        obj.generate_key()
        import pdb; pdb.set_trace()
