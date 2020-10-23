import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    """Create Question model in poll application."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date expired')

    def __str__(self):
        """Return str of the Question text."""
        return self.question_text

    def was_published_recently(self):
        """Check The question was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check The question is published."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check The question that can vote."""
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Create Choices model in poll application."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return str of choice text."""
        return self.choice_text

class User(models.Model):
    """User's model"""
    username = models.CharField(max_length=254)
    password = models.CharField(max_length=254)

