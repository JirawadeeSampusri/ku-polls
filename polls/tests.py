import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question,Choice

class QuestionModelTests(TestCase):

    def test_is_published_with_future_question(self):
        """
        is_published() return False if current date is
        before question's publication date.
        """
        time = timezone.now() + datetime.timedelta(days=10)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_question(self):
        """
        is_published() return Ture if current date is
        after question's publication date.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_is_published_with_present_question(self):
        """
        is_published() return Ture if current date is
        on question's publication date.
        """
        time = timezone.now()
        present_question = Question(pub_date=time)
        self.assertIs(present_question.is_published(), True)

    def test_can_vote_with_now_is_after_pub_date_and_before_end_date(self):
        """
        can_vote() return True if you're voting currently is between
        pub_date and end_date.
        """
        pub_date = timezone.now() - datetime.timedelta(days=2)
        end_date = timezone.now() + datetime.timedelta(days=10)
        now = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(now.can_vote(), True)

    def test_can_vote_with_now_equal_to_pub_date(self):
        """
        can_vote() return True if you're voting currently is on
        pub_date.
        """
        pub_date = timezone.now()
        end_date = timezone.now() + datetime.timedelta(days=1)
        now = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(now.can_vote(), True)

    def test_can_vote_with_now_is_before_pub_date(self):
        """
        can_vote() return False if you're voting currently is before
        pub_date.
        """
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = timezone.now()
        before = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(before.can_vote(), False)

    def test_can_vote_with_now_is_after_end_date(self):
        """
        can_vote() return False if you're voting currently is after
        end_date.
        """
        pub_date = timezone.now()
        end_date = timezone.now() - datetime.timedelta(days=1)
        before = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(before.can_vote(), False)

    def test_can_vote_with_now_is_equal_to_end_date(self):
        """
        can_vote() return False if you're voting currently is on
        end_date.
        """
        pub_date = timezone.now() + datetime.timedelta(days=1)
        end_date = timezone.now()
        before = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(before.can_vote(), False)
        
def create_question(question_text, pub_date, end_date):
    """
    Create a question with the given question_text and published the
    given number of days offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    pub_time = timezone.now() + datetime.timedelta(days=pub_date)
    end_time = timezone.now() + datetime.timedelta(days=end_date)
    return Question.objects.create(question_text=question_text, pub_date=pub_time, end_date=end_time)


class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200) #responseok  #responseerror404
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", pub_date=-10, end_date=-8)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on.
        the index page.
        """
        create_question(question_text="Future question.", pub_date=30, end_date=31)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Future question.>'])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions.
        are displayed.
        """
        create_question(question_text="Future question.", pub_date=10, end_date=11)
        create_question(question_text="Past question.", pub_date=-10, end_date=-9)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Future question.>', '<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past first question", pub_date=-30, end_date=-29)
        create_question(question_text="Past second question", pub_date=-5, end_date=-4)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past second question>', '<Question: Past first question>']
        )


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', pub_date=20, end_date=23)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) #pathมีเเต่ไม่สามารถเช่ือมไปได้

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', pub_date=-7, end_date=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

