import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse

from .models import Question

class QuestionModelTests(TestCase):
    
    def setUp(self):
        self.question = Question(question_text='Quien es el mejor Course Director de Platzi.')
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), False)
        
    def test_was_published_recently_with_present_question(self):
        """was_publised_present returns True for questions whose pub_date is in the present"""
        time = timezone.now()
        self.question.pub_date = time
        self.assertIs(self.question.was_published_recently(), True)
        
    def test_was_published_past(self):
        """was publised_past returns False for Questions whose is in the more 1 day in the past"""
        time1 = timezone.now() - datetime.timedelta(days=2)
        self.question.pub_date = time1
        self.assertIs(self.question.was_published_recently(), False)
        

def created_question(text, days):
    """Create a question in te future o past"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)

class QuestionIndexViewTest(TestCase):
    
    def test_no_questions(self):
        """If no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_future_question(self):
        """Question published in the future, are't published in the index"""
        created_question('future', 15)       
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])
    
    def test_past_question(self):
        """Question published in the past, are published in the index"""
        question = created_question('past', -15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],[question])
        
    def test_future_question_and_past_question(self):
        """Even if both past and future question exist, only past questions are displayed"""
        past_question = created_question('past question', -30)
        future_question = created_question('future question', 15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question]
        )
    
    def test_two_past_question(self):
        """The questions index page may display multiple questions"""
        past_question1 = created_question('past1 question', -30)
        past_question2 = created_question('past2 question', -40)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [past_question1,past_question2]
        )
    
    def test_two_future_question(self):
        """The question index page is void"""
        future_question1 = created_question('future1 question', 10)
        future_question2 = created_question('future2 question', 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future
        returns a 404 error not found"""
        future_question = created_question('future Question', 30)
        url = reverse('polls:detail', args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """The detail view of a question with a pub_date in the past
        displays the questions text"""
        past_question = created_question('past Question', -30)
        url = reverse('polls:detail', args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

"""
Desafío: perfecciona tus habilidades
1. Crea los tests para ResultsView.
2. Asegúrate de que no se pueden crear Questions sin Choices.
3. Crea los tests respectivos.
"""
