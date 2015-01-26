from django.conf import settings
from rest_framework.test import APIClient, APITestCase
from shortener.models import URLPair


class URLShortenerTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    # test key word = abidjan
    def test_simple_word_in_url(self):
        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com/2012/12/abidjan/'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('original_url'), 'http://techcrunch.com/2012/12/abidjan/')
        self.assertEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/abidjan/')

    # test key word = pinterest-abet
    def test_complicated_word_in_url(self):
        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com/2012/12/10/pinterest-abet/'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('original_url'), 'http://techcrunch.com/2012/12/10/pinterest-abet/')
        self.assertEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/abet/')

    # test key word = abram, which is already used before.
    def test_word_in_url_used_and_need_to_pick_random_word(self):
        URLPair.objects.create_url_pair('http://techcrunch.com/2012/12/abram/')

        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com/2012/abram/'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('original_url'), 'http://techcrunch.com/2012/abram/')
        self.assertNotEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/abram/')
        print response.context[0].get('shortened_url')

    # test the URL which was shortened before
    def test_existing_url_input(self):
        URLPair.objects.create_url_pair('http://techcrunch.com/20/pier/')

        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com/20/pier/'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('original_url'), 'http://techcrunch.com/20/pier/')
        self.assertEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/pier/')

    # test 2 key words = pig & pile, both were used before.
    def test_words_in_url_input_used_and_need_to_pick_random_word(self):
        URLPair.objects.create_url_pair('http://fb.com/12/34/56/pig/')
        URLPair.objects.create_url_pair('http://fb.com/12/34/56/pile/')

        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com/2012/pig-pile/'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('original_url'), 'http://techcrunch.com/2012/pig-pile/')
        self.assertNotEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/pig/')
        self.assertNotEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/pile/')
        print response.context[0].get('shortened_url')

    # test a key word = lalalallalalaal, which is not in wordslist
    def test_word_in_url_input_not_existing_in_wordslist(self):
        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com/2012/lalalallalalaal/'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('original_url'), 'http://techcrunch.com/2012/lalalallalalaal/')
        self.assertNotEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/lalalallalalaal/')
        print response.context[0].get('shortened_url')

    # test all words in wordslist were used
    # def test_all_words_in_wordslsit_are_used(self):
    #     URLPair.objects.all().delete()
    #     URLPair.objects.create_url_pair('http://fb.com/12/34/56/wop/')
    #     URLPair.objects.create_url_pair('http://fb.com/12/34/56/worcester/')
    #     URLPair.objects.create_url_pair('http://fb.com/12/34/56/word/')
    #     URLPair.objects.create_url_pair('http://fb.com/12/34/56/wordsworth/')
    #     URLPair.objects.create_url_pair('http://fb.com/12/34/56/wordy/')
    #
    #     response = self.client.post('/shorten_url/',
    #                                 {'url_input': 'http://techcrunch.com/2012/lalalallalalaal/'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context[0].get('original_url'), 'http://techcrunch.com/2012/lalalallalalaal/')
    #     self.assertNotEqual(response.context[0].get('shortened_url'), 'http://myurlshortener.com/wop/')

    # test an invalid URL input
    def test_invalid_url_input(self):
        response = self.client.post('/shorten_url/',
                                    {'url_input': 12345})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('message'), 'The input URL is invalid.')

    # test URL input missing
    def test_missing_url_input(self):
        response = self.client.post('/shorten_url/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('message'), 'The input URL is invalid.')

    # test an invalid URL input, there is a space in URL
    def test_invalid_url_input_with_space_inside(self):
        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com/2012/12/an  na/'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('message'), 'The input URL is invalid.')

    # test a URL input, which is not able to shorten
    def test_url_input_unshortenable(self):
        response = self.client.post('/shorten_url/',
                                    {'url_input': 'http://techcrunch.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[0].get('message'), 'The input URL is unshortenable.')

    # test request method is get
    def test_get_method(self):
        response = self.client.get('/shorten_url/',
                                   {'url_input': 'http://techcrunch.com/la/34/liy/'})
        self.assertEqual(response.status_code, 200)





