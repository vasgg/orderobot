import unittest
from unittest import IsolatedAsyncioTestCase, TestCase

from core.controllers.application_controllers import toggle_application_activeness
from core.controllers.order_controllers import validate_url
from core.database.db import db


class Test(TestCase):
    def test_valid_url(self):
        # Test with valid URLs
        self.assertTrue(validate_url('https://drive.google.com/some/path'))
        self.assertTrue(validate_url('http://drive.yandex.ru/another/path'))
        self.assertTrue(validate_url('drive.google.com/some/path'))
        self.assertTrue(validate_url('drive.yandex.ru/another/path'))

    def test_invalid_url(self):
        # Test with invalid URLs
        self.assertFalse(validate_url('https://www.example.com'))
        self.assertFalse(validate_url('http://localhost:8000'))

    def test_empty_url(self):
        # Test with an empty string
        self.assertFalse(validate_url(''))

    def test_malformed_url(self):
        # Test with a malformed URL
        self.assertFalse(validate_url('htp:/malformed.url'))


class Test2(IsolatedAsyncioTestCase):
    async def test_get_orders(self):
        async with db.session_factory.begin() as session:
            application = await toggle_application_activeness(application_id=13, session=session)

        print(application)
        # self.fail()
        await db.engine.dispose()
