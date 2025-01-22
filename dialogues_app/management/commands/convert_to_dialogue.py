from django.core.management.base import BaseCommand
from dialogues_app.models import ClientQuestion


class Command(BaseCommand):
    help = 'Converts existing questions and answers to dialogue format'

    def handle(self, *args, **options):
        questions = ClientQuestion.objects.all()
        converted = 0

        for q in questions:
            if q.question and q.answer:
                dialogue = f"User: {q.question}\nAssistant: {q.answer}"
                q.dialogue_example = dialogue
                q.save()
                converted += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully converted {converted} records'
            )
        )