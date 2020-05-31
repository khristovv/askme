from django.test import TestCase
from questions.forms import PostQuestionForm, AnswerQuestionForm


class TestPostQuestionForm(TestCase):
    def test_question_text_more_than_max_length(self):
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


class TestAnswerQuestionForm(TestCase):
    def test_answer_text_more_than_max_length(self):
        form = AnswerQuestionForm(data={
            'content': 'A'*1026
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.clean(), {})

    def test_form_can_accept_unicode_characters(self):
        form = AnswerQuestionForm(data={
            'content': 'Отговор'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean(), {
            'content': 'Отговор'
        })

    def test_valid_form(self):
        form = AnswerQuestionForm(data={
            'content': 'A cool answer'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.clean(), {
            'content': 'A cool answer'
        })
