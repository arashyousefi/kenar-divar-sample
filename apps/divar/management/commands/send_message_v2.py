from django.core.management import BaseCommand

from apps.divar.client import DivarClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Sending message to Divar...")
        c = DivarClient()
        token = ""
        ok, response = c.request_conversation_send_message("9c19c900-cc81-4ef5-a627-e51e87a1dab6", "hello", token)
        print(response)
        print(ok)
        print("Done!")
