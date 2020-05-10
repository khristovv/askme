from django.test import TestCase
from questions.forms import PostQuestionForm


class TestPostQuestionForm(TestCase):
    def test_question_test_more_than_max_length(self):
        form = PostQuestionForm(data={
            'question_text': 'A'*514,
            'is_anonymous': True
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.clean(), {
            'is_anonymous': True
        })

    def test_form_can_accept_unicode_characters(self):
        form = PostQuestionForm(data={
            'question_text': 'Въпрос?',
            'is_anonymous': False
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean(), {
            'question_text': 'Въпрос?',
            'is_anonymous': False
        })

    def test_valid_form(self):
        form = PostQuestionForm(data={
            'question_text': 'A cool question?',
            'is_anonymous': True
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean(), {
            'question_text': 'A cool question?',
            'is_anonymous': True
        })
