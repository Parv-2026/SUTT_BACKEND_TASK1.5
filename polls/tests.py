"""Automated tests covering the official tutorial's key behaviors."""
import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Choice, Question


def create_question(text, days):
    return Question.objects.create(question_text=text, pub_date=timezone.now() + datetime.timedelta(days=days))


class QuestionModelTests(TestCase):
    def test_recent_future_question_is_not_recent(self):
        question = create_question('Future?', 30)
        self.assertIs(question.was_published_recently(), False)

    def test_old_question_is_not_recent(self):
        question = create_question('Old?', -2)
        self.assertIs(question.was_published_recently(), False)

    def test_recent_question_is_recent(self):
        question = create_question('Recent?', -0.5)
        self.assertIs(question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available yet.')
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_question_visible(self):
        question = create_question('Past question', -1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_question_hidden(self):
        create_question('Future question', 1)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available yet.')

    def test_only_five_latest_questions(self):
        for i in range(7):
            create_question(f'Question {i}', -i-1)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(len(response.context['latest_question_list']), 5)


class QuestionDetailViewTests(TestCase):
    def test_future_question_is_404(self):
        future_question = create_question('Future', 3)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question_visible(self):
        past_question = create_question('Past', -1)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, 'Past')


class VotingTests(TestCase):
    def setUp(self):
        self.question = create_question('Favorite topic?', -1)
        self.choice = Choice.objects.create(question=self.question, choice_text='Backend', votes=0)
        self.url = reverse('polls:vote', args=(self.question.id,))

    def test_vote_increments_count_and_redirects(self):
        response = self.client.post(self.url, {'choice': str(self.choice.id)})
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)

    def test_no_choice_shows_error(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You did not select a valid choice.')
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)

    def test_invalid_choice_shows_error(self):
        response = self.client.post(self.url, {'choice': '9999'})
        self.assertContains(response, 'You did not select a valid choice.')

    def test_get_cannot_cast_vote(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)

    def test_future_question_cannot_be_voted_on(self):
        future = create_question('Not yet available', 1)
        choice = Choice.objects.create(question=future, choice_text='Yes')
        self.assertEqual(self.client.post(reverse('polls:vote', args=(future.pk,)), {'choice': choice.pk}).status_code, 404)
