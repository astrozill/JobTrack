from unittest.mock import patch

from django.db import OperationalError
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(SECURE_SSL_REDIRECT=False)
class ReadinessCheckTests(TestCase):

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_http_readiness_reaches_database_check_with_https_enabled(self):
        response = self.client.get(reverse('readiness_check'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_http_readiness_returns_503_with_https_enabled_and_database_unavailable(self):
        with patch('jobtrack.urls.connection.cursor', side_effect=OperationalError('database unavailable')):
            response = self.client.get(reverse('readiness_check'))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content, b'Not ready')

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_other_http_routes_still_redirect_to_https(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response['Location'], 'https://testserver/accounts/login/')


    def test_ready_when_database_is_available(self):
        response = self.client.get(reverse('readiness_check'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')
        self.assertIn('no-store', response['Cache-Control'])

    def test_not_ready_when_database_is_unavailable(self):
        with patch('jobtrack.urls.connection.cursor', side_effect=OperationalError('private database details')):
            response = self.client.get(reverse('readiness_check'))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content, b'Not ready')
        self.assertIn('no-store', response['Cache-Control'])

    def test_not_ready_when_database_query_fails(self):
        with patch('jobtrack.urls.connection.cursor') as cursor:
            cursor.return_value.__enter__.return_value.execute.side_effect = OperationalError('query failed')
            response = self.client.get(reverse('readiness_check'))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content, b'Not ready')

    @override_settings(SECURE_SSL_REDIRECT=True)

    def test_health_check_is_available_without_database(self):
        with patch('jobtrack.urls.connection.cursor', side_effect=OperationalError('database unavailable')):
            response = self.client.get(reverse('health_check'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'OK')
