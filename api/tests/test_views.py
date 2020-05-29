"""
Модуль тестов на views
"""
import datetime

import redis
from freezegun import freeze_time
from unittest.mock import patch
from rest_framework.test import APITestCase, APIClient


class PostVisitsAPITests(APITestCase):
    """
    Класс теста основных функций PostVisitsView
    """
    def setUp(self):
        """
        Метод инициализации тестов
        """
        self.client = APIClient()

        # Создание экземпляра Redis для тестов
        self.test_redis = redis.Redis(host='localhost', port=6379, db=1)

    @freeze_time(datetime.datetime.utcfromtimestamp(1590689100))
    def test_post_single_valid_visit(self):
        """
        Тест на передачу одной валидной ссылки
        """
        data = {
            'links': [
                'https://ya.ru?q=12345'
            ]
        }

        with patch('redis.Redis', return_value=self.test_redis):
            response = self.client.post('/api/visited_links', data)

        redis_data_bytes = self.test_redis.smembers('1590689100')
        redis_data_str = [x.decode('utf-8') for x in redis_data_bytes]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('status'), 'ok')
        self.assertCountEqual(redis_data_str, data.get('links'))

        self.test_redis.flushdb()

    @freeze_time(datetime.datetime.utcfromtimestamp(1590689200))
    def test_post_valid_visits(self):
        """
        Тест на передачу нескольких валидных ссылок
        """
        data = {
            'links': [
                'https://ya.ru',
                'https://ya.ru?q=123',
                'funbox.ru',
                'https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor'
            ]
        }

        with patch('redis.Redis', return_value=self.test_redis):
            response = self.client.post('/api/visited_links', data)

        redis_data_bytes = self.test_redis.smembers('1590689200')
        redis_data_str = [x.decode('utf-8') for x in redis_data_bytes]

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('status'), 'ok')
        self.assertCountEqual(redis_data_str, data.get('links'))

        self.test_redis.flushdb()

    def test_post_invalid_visits(self):
        """
        Тест на передачу запроса, не содержащего ключ 'links'
        """
        with patch('redis.Redis', return_value=self.test_redis):
            response = self.client.post('/api/visited_links', {'fruits': 'apple'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('status'), 'JSON must have "links" key')


class GetDomainsAPITests(APITestCase):
    """
    Класс теста основных функций GetDomainsView
    """
    def setUp(self):
        """
        Метод инициализации тестов
        """
        self.client = APIClient()

        # Создание экземпляра Redis для тестов
        self.test_redis = redis.Redis(host='localhost', port=6379, db=1)

    def test_get_domains(self):
        """
        Тест на получение списка уникальных доменов, посещенных за переданный интервал времени
        """
        self.test_redis.sadd('1500000000', 'https://www.youtube.com/' 'https://www.google.com/')
        self.test_redis.sadd('1500000120', 'https://www.instagram.com/funboxteam/')
        self.test_redis.sadd('1500000160', 'https://habr.com/ru/' 'instagram.com/anton_lapenko/?hl=ru')

        with patch('redis.Redis', return_value=self.test_redis):
            response = self.client.get('/api/visited_domains?from=1500000100&to=1500000200')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('status'), 'ok')
        self.assertCountEqual(list(response.data.get('domains')), ['instagram.com', 'habr.com'])

        self.test_redis.flushdb()

    def test_get_domains_without_time_interval(self):
        """
        Тест на получение списка уникальных доменов без переданного интервала времени
        """
        with patch('redis.Redis', return_value=self.test_redis):
            response = self.client.get('/api/visited_domains')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('status'), 'Request must contain a valid time interval')

    def test_get_domains_with_invalid_intervals(self):
        """
        Тест на получение списка уникальных доменов без переданного валидного интервала времени
        """
        with patch('redis.Redis', return_value=self.test_redis):
            response = self.client.get('/api/visited_domains?from=invalid&to=interval')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get('status'), 'Request must contain a valid time interval')
