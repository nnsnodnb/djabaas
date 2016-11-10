# coding=utf-8

from django.test.client import Client
from django.test import TestCase
from push.views import *

class UrlResolveTests(TestCase):
    def test_url_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 302)

    def test_url_index_page(self):
        c = Client()
        response = c.get('/', {'page': 2})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content, '')
