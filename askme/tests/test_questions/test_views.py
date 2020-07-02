import json

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


class TestToggleLike(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_superuser(email='user1@mail.com', username='user1', password='asdasdasd')
        self.user2 = User.objects.create_superuser(email='user2@mail.com', username='user2', password='asdasdasd')
        self.u1_q1 = Question.objects.create(content='question 1 to user1?', asked_by=self.user2, asked_to=self.user1)
        self.u2_q1 = Question.objects.create(content='question 1 to user2?', asked_by=self.user1, asked_to=self.user2)
        self.u1_q1_answer = Answer.objects.create(question=self.u1_q1, content='answer to question1 of user1')
        self.u2_q1_answer = Answer.objects.create(question=self.u2_q1, content='answer to question1 of user2')

    def test_when_toggle_like_receives_a_valid_POST_request_then_preform_toggle_logic(self):
        self.client.force_login(self.user1)

        self.assertEqual(len(self.user1.liked_questions.all()), 0)

        response = self.client.post(reverse('toggle_like'), {
            'answer_id': self.u2_q1_answer.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.user1.liked_questions.all()), 1)
        self.assertTrue(self.user1 in self.u2_q1_answer.likes.all())
        self.assertEqual(json.loads(response.content), {"liked": True})

        # user likes his own question
        response = self.client.post(reverse('toggle_like'), {
            'answer_id': self.u1_q1_answer.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.user1.liked_questions.all()), 2)
        self.assertTrue(self.user1 in self.u1_q1_answer.likes.all())
        self.assertEqual(json.loads(response.content), {"liked": True})

        # when pressing a like button that has already been pressed then remove like from answer
        response = self.client.post(reverse('toggle_like'), {
            'answer_id': self.u2_q1_answer.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.user1.liked_questions.all()), 1)
        self.assertFalse(self.user1 in self.u2_q1_answer.likes.all())
        self.assertEqual(json.loads(response.content), {"liked": False})

        response = self.client.post(reverse('toggle_like'), {
            'answer_id': self.u1_q1_answer.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.user1.liked_questions.all()), 0)
        self.assertFalse(self.user1 in self.u1_q1_answer.likes.all())
        self.assertEqual(json.loads(response.content), {"liked": False})

    def test_when_toggle_like_receives_GET_instead_of_POST_then_return_405(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse('toggle_like'), {
                'answer_id': self.u2_q1_answer.id
            })
        self.assertEqual(response.status_code, 405)
        self.assertEqual(len(self.user1.liked_questions.all()), 0)
        self.assertFalse(self.user1 in self.u2_q1_answer.likes.all())

    def test_when_not_authenticated_user_attempts_to_like_answer_then_redirect_to_login_page(self):
        response = self.client.post(reverse('toggle_like'), {
            'answer_id': self.u2_q1_answer.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/like/')
        self.assertEqual(len(self.user1.liked_questions.all()), 0)
        self.assertFalse(self.user1 in self.u2_q1_answer.likes.all())
