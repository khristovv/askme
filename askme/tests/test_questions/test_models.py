from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model

from questions.models import Question, Like, Answer


class TestQuestion(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user('user1@mail.com', 'user1', 'A-S@fe-p@$$word')
        self.user2 = self.User.objects.create_user('user2@mail.com', 'user2', 'A-S@fe-p@$$word')

    def test_reverse_relations_of_question(self):
        Question.objects.create(
            asked_by=self.user1,
            asked_to=self.user2,
            content='Is this a good test?'
        )

        Question.objects.create(
            asked_by=None,
            asked_to=self.user2,
            content='Is this a good test?'
        )
        Question.objects.create(
            asked_by=self.user2,
            asked_to=self.user1,
            content='Is this a good test?'
        )

        self.assertEqual(len(self.user1.questions_received.all()), 1)
        self.assertEqual(len(self.user2.questions_received.all()), 2)
        self.assertEqual(len(self.user1.questions_posted.all()), 1)
        self.assertEqual(len(self.user1.questions_posted.all()), 1)


class TestAnswer(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user('user1@mail.com', 'user1', 'A-S@fe-p@$$word')
        self.user2 = self.User.objects.create_user('user2@mail.com', 'user2', 'A-S@fe-p@$$word')
        self.q1 = Question.objects.create(
            asked_by=self.user1,
            asked_to=self.user2,
            content='Is this a good test?'
        )
        self.q2 = Question.objects.create(
            asked_by=self.user2,
            asked_to=self.user1,
            content='How about this one?'
        )
        self.q3 = Question.objects.create(
            asked_by=None,
            asked_to=self.user1,
            content='Am I cool?'
        )

    def test_reverse_relation_of_answer(self):
        Answer.objects.create(question=self.q1, content='no1')
        Answer.objects.create(question=self.q2, content='no2')
        Answer.objects.create(question=self.q3, content='no3')

        self.assertEqual(self.q1.answer.content, 'no1')
        self.assertEqual(self.q2.answer.content, 'no2')
        self.assertEqual(self.q3.answer.content, 'no3')


class TestLike(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user1 = self.User.objects.create_user('user1@mail.com', 'user1', 'A-S@fe-p@$$word')
        self.user2 = self.User.objects.create_user('user2@mail.com', 'user2', 'A-S@fe-p@$$word')
        self.q1 = Question.objects.create(
            asked_by=self.user1,
            asked_to=self.user2,
            content='Is this a good test?'
        )
        self.q2 = Question.objects.create(
            asked_by=self.user2,
            asked_to=self.user1,
            content='How about this one?'
        )

        self.a1 = Answer.objects.create(
            question=self.q1,
            content='No, bro'
        )

        self.a2 = Answer.objects.create(
            question=self.q2,
            content='Still bad'
        )

    def test_liking_the_same_answer_twice_violates_unique_constraints(self):
        Like.objects.create(answer=self.a1, user=self.user1)
        l2 = Like(answer=self.a1, user=self.user1)
        self.assertRaises(IntegrityError, l2.save)

    def test_reverse_relations_of_like(self):
        Like.objects.create(answer=self.a1, user=self.user1)
        Like.objects.create(answer=self.a2, user=self.user2)
        Like.objects.create(answer=self.a2, user=self.user1)

        self.assertEqual(len(self.user2.liked_answers.all()), 1)
        self.assertEqual(len(self.user1.liked_answers.all()), 2)

        self.assertEqual(len(self.a1.likes.all()), 1)
        self.assertEqual(len(self.a2.likes.all()), 2)



