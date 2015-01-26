from unittest import TestCase
from shortener.models import URLPair


class TestPickingWordAlgorithm(TestCase):
    def setUp(self):
        self.populate_database()

    def populate_database(self):
        URLPair.objects.all().delete()
        URLPair.objects.create_url_pair('http://techcrunch.com/2012/12/zoom/')
        URLPair.objects.create_url_pair('http://techcrunch.com/2012/12/your/')
        URLPair.objects.create_url_pair('http://techcrunch.com/20/12/youth/')

    def test_create_a_new_url_pair(self):
        URLPair.objects.create_url_pair('http://techcrunch.com/20/12/zurich/')
        self.assertEqual(URLPair.objects.all().count(), 4)

    def test_key_word_used_before_thus_picking_a_random_word(self):
        URLPair.objects.create_url_pair('http://techcrunch.com/20/55/youth/')
        self.assertEqual(URLPair.objects.all().count(), 4)

    def test_key_word_not_in_wordslist_thus_picking_a_random_word(self):
        URLPair.objects.create_url_pair('http://techcrunch.com/20/55/lololololololo/')
        self.assertEqual(URLPair.objects.all().count(), 4)

    def test_2_key_words_used_before_thus_picking_a_random_word(self):
        URLPair.objects.create_url_pair('http://techcrunch.com/20/55/zoom_your/')
        self.assertEqual(URLPair.objects.all().count(), 4)

    def test_2_key_words_one_used_and_another_one_is_new(self):
        URLPair.objects.create_url_pair('http://techcrunch.com/20/55/zoom/yon/')
        self.assertEqual(URLPair.objects.all().count(), 4)


