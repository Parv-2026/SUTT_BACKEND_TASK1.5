"""Populate a few example polls for demonstrations (safe to rerun)."""
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from polls.models import Question, Choice


class Command(BaseCommand):
    help = 'Create example poll questions and choices.'

    def handle(self, *args, **options):
        examples = [
            ('Which campus event would you attend?', ['Tech talk', 'Music night', 'Sports tournament']),
            ('What should the next workshop focus on?', ['Python', 'Web development', 'Data structures']),
        ]
        for question_text, choice_texts in examples:
            question, created = Question.objects.get_or_create(
                question_text=question_text,
                defaults={'pub_date': timezone.now() - datetime.timedelta(hours=1)},
            )
            for choice_text in choice_texts:
                Choice.objects.get_or_create(question=question, choice_text=choice_text)
            self.stdout.write(self.style.SUCCESS(('Created' if created else 'Exists') + ': ' + question_text))
