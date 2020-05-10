from django.test import TestCase
from django.urls import reverse

from users.models import User
from questions.models import Question, Answer


class TestBoardView(TestCase):
    def setUp(self):
        self.user1 = User(email='user1@mail.com', username='user1', password='asdasdasd', is_active=True)
        self.user1.save()
        self.user2 = User(email='user2@mail.com', username='user2', password='asdasdasd', is_active=True)
        self.user2.save()

    def test_when_user_not_logged_then_dont_save_question_and_redirect_to_login_page(self):
        response = self.client.post(reverse('board', kwargs={'username': 'user2'}), {
            'question_text': "Won't be saved in the database",
            'is_anonymous': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')
        self.assertEqual(len(Question.objects.all()), 0)

    def test_when_user_logged_in_and_question_is_anonymous_then_save_question_with_asked_by_equal_to_none(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('board', kwargs={'username': 'user2'}), {
            'question_text': "Will be saved in the database",
            'is_anonymous': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.get(asked_to=self.user2).content, "Will be saved in the database")
        self.assertEqual(Question.objects.get(asked_to=self.user2).asked_by, None)

    def test_when_user_logged_in_and_question_is_not_anonymous_then_save_question_with_asked_by_user1(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('board', kwargs={'username': 'user2'}), {
            'question_text': "Will be saved in the database",
            'is_anonymous': False
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.get(asked_to=self.user2).content, "Will be saved in the database")
        self.assertEqual(Question.objects.get(asked_to=self.user2).asked_by, self.user1)

    def test_when_question_text_more_than_max_length_then_dont_save_question(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('board', kwargs={'username': 'user2'}), {
            'question_text': "A"*1000,
            'is_anonymous': False
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Question.objects.all()), 0)

    def test_when_user2_has_2_public_questions_then_render_tempalte_with_2_questions(self):
        self.client.force_login(self.user1)
        q1 = Question.objects.create(asked_by=self.user1, asked_to=self.user2, content='question 1 ?')
        q2 = Question.objects.create(asked_by=self.user1, asked_to=self.user2, content='question 2 ?')
        Answer.objects.create(question=q1, content='yes')
        Answer.objects.create(question=q2, content='no')
        response = self.client.get(reverse('board', kwargs={'username': 'user2'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['questions']), 2)
        self.assertQuerysetEqual(response.context['questions'], [repr(q1), repr(q2)], ordered=False)

    def test_when_user2_has_1_public_and_1_hidden_question_then_render_tempalte_with_1_only_public_question(self):
        self.client.force_login(self.user1)
        q1 = Question.objects.create(asked_by=self.user1, asked_to=self.user2, content='question 1 ?')
        q2 = Question.objects.create(asked_by=self.user1, asked_to=self.user2, content='question 2 ?', hidden=True)
        Answer.objects.create(question=q1, content='yes')
        Answer.objects.create(question=q2, content='no')
        response = self.client.get(reverse('board', kwargs={'username': 'user2'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['questions']), 1)
        self.assertQuerysetEqual(response.context['questions'], [repr(q1)], ordered=False)


