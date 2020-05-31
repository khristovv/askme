from django.test import TestCase
from django.urls import reverse

from questions.models import Question, Answer
from users.models import User


class TestAnswerQuestion(TestCase):
    def setUp(self):
        self.user1 = User(email='user1@mail.com', username='user1', password='asdasdasd', is_active=True)
        self.user1.save()
        self.user2 = User(email='user2@mail.com', username='user2', password='asdasdasd', is_active=True)
        self.user2.save()
        self.u1_q1 = Question(content='question 1 to user1?', asked_by=self.user2, asked_to=self.user1)
        self.u1_q1.save()
        self.u2_q1 = Question(content='question 1 to user2?', asked_by=self.user1, asked_to=self.user2)
        self.u2_q1.save()

    def test_save_answer_on_successful_post_request(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('answer_question', kwargs={'question_id': self.u1_q1.id}), {
            'content': 'Answer of question of user1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/inbox/')
        self.assertEqual(Answer.objects.get(question=self.u1_q1).content,  'Answer of question of user1')
        self.client.logout()

        self.client.force_login(self.user2)
        response = self.client.post(reverse('answer_question', kwargs={'question_id': self.u2_q1.id}), {
            'content': 'Answer of question of user2'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/inbox/')
        self.assertEqual(Answer.objects.get(question=self.u2_q1).content,  'Answer of question of user2')

        self.assertEqual(len(Answer.objects.all()), 2)

    def test_when_user1_tries_to_access_question_of_user2_then_deny_access(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('answer_question', kwargs={'question_id': self.u2_q1.id}), {
            'content': 'Answer will not be saved'
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(Answer.objects.all()),  0)

    def test_when_user1_tries_to_access_non_existing_question_then_return_404_response(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('answer_question', kwargs={'question_id': 10}), {
            'content': 'Answer will not be saved'
        })
        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(Answer.objects.all()),  0)

    def test_when_user1_posts_invalid_form_data_then_dont_save_answer(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('answer_question', kwargs={'question_id': self.u1_q1.id}), {
            'content': 'Answer will not be saved'*1026
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Answer.objects.all()),  0)
