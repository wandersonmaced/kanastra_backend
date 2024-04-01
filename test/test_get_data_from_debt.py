import unittest
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from unittest.mock import MagicMock

from file_handling.model.file_models import Debt
from file_handling.views.debt import DebtListView

class TestDebtListView(APITestCase):

    def setUp(self):

        Debt.objects.create(name='Debt 1', amount=100)
        Debt.objects.create(name='Debt 2', amount=200)
        Debt.objects.create(name='Debt 3', amount=300)

        self.view = DebtListView()

    def test_get_paginated_debt_list(self):
        factory = APIRequestFactory()
        request = factory.get('/debt/')
        request.query_params = MagicMock(return_value={})
        self.view.request = request

        response = self.view.get(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_pagination(self):
        factory = APIRequestFactory()
        request = factory.get('/debt/')
        request.query_params = MagicMock(return_value={})
        self.view.request = request

        response = self.view.get(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    def test_page_size_query_param(self):
        factory = APIRequestFactory()
        request = factory.get('/debt/', {'page_size': 2})
        request.query_params = MagicMock(return_value={'page_size': 2})
        self.view.request = request

        response = self.view.get(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

if __name__ == '__main__':
    unittest.main()
