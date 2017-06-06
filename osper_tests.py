# -*- coding: utf-8 -*-
import unittest
import mock
import osper_test_fixtures

import os
import osper
import tempfile

@mock.patch('braintree.ClientToken.generate', staticmethod(lambda: 'test_client_token'))
class AppTestCase(unittest.TestCase):

    def setUp(self):
        osper.app.config['TESTING'] = True
        self.app = osper.app.test_client()

    @mock.patch('braintree.Transaction.search', staticmethod(osper_test_fixtures.successful_search))
    @mock.patch('braintree.Transaction.sale', staticmethod(lambda x: osper_test_fixtures.MockObjects.TRANSACTION_SALE_SUCCESSFUL))
    def test_successful_load(self):
        res = self.app.post('/load', data={
            'amount': '12.34',
            'customer_id': '000001',
            'payment_method_nonce': 'some_nonce',
        })
        self.assertEqual(res.status_code, 200)

    @mock.patch('braintree.Transaction.search', staticmethod(osper_test_fixtures.one_day_failure_search))
    def test_one_day_failure(self):
        res = self.app.post('/load', data={
            'amount': '12.34',
            'customer_id': '000001',
            'payment_method_nonce': 'some_nonce',
        })
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
