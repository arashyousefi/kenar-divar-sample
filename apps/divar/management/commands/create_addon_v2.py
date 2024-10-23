from django.core.management import BaseCommand

from apps.divar.client import DivarClient
from apps.divar.models import TempAuthorizationData


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Creating addon V2...")
        c = DivarClient()
        post_token = "wZDwv-vo"
        a = TempAuthorizationData.objects.get(scope__contains=post_token)
        ok, response = c.request_set_credit_score_to_post_v2(None, 1, a, post_token)
        print(response)
        print(ok)
        print("Done!")