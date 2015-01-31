import random
from urlparse import urlparse
from django.contrib.auth.models import BaseUserManager
from django.db import models
from model_utils.models import TimeStampedModel
from django.conf import settings
import re


class URLPairManager(BaseUserManager):
    def _create_url_pair_with_random_picking(self, read_data, original_url):
        """
        Creates and saves a URLPair by picking a random word from cleaned_words.txt
        """
        key = random.choice(read_data)
        url_pair = self.model(key=key,
                              original_url=original_url,
                              shortened_url=settings.BASE_URL + key + '/')
        url_pair.full_clean()
        url_pair.save()
        return url_pair

    def create_url_pair(self, original_url):
        """
        Creates and saves a URLPair with the given original_url
        """
        read_data = [line.rstrip() for line in open(settings.PROJECT_ROOT + settings.TEST_DATA_PATH, 'r')]
        parse_original_url = urlparse(original_url)

        words_list_from_original_url = re.findall(r"[\w']+", parse_original_url.path)
        tmp_words_list = []

        for w in words_list_from_original_url:
            if w in read_data:
                if not URLPair.objects.filter(key=w).exists():
                    key = w
                    url_pair = self.model(key=key,
                                          original_url=original_url,
                                          shortened_url=settings.BASE_URL + key + '/')
                    url_pair.full_clean()
                    url_pair.save()
                    return url_pair
                else:
                    tmp_words_list.append(w)

        if len(tmp_words_list) != 0:
            for w in tmp_words_list:
                read_data.remove(w)
            return self._create_url_pair_with_random_picking(read_data, original_url)

        return self._create_url_pair_with_random_picking(read_data, original_url)


class URLPair(TimeStampedModel, models.Model):
    original_url = models.URLField(max_length=1000)
    shortened_url = models.URLField()
    key = models.CharField(max_length=200)

    objects = URLPairManager()

    def __unicode__(self):
        return self.key + ' : ' + self.original_url
