# backend/postgresql_app/tests.py

from django.test import TestCase
from .models import Joke

class JokeModelTest(TestCase):
    def setUp(self):
        Joke.objects.create(content="Test joke", added_at="2024-09-01T12:00:00Z")

    def test_joke_content(self):
        joke = Joke.objects.get(content="Test joke")
        self.assertEqual(joke.content, "Test joke")

