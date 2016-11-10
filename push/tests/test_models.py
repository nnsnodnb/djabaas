# coding=utf-8

from django.test import TestCase
from push.models import DeviceTokenModel, NotificationModel, DevelopFileModel, ProductFileModel
from datetime import datetime

class DeviceTokenModelTests(TestCase):
    def test_is_empty(self):
        saved_device_token = DeviceTokenModel.objects.all()
        self.assertEqual(saved_device_token.count(), 0)

    def test_is_not_empty(self):
        device_token = DeviceTokenModel(os_version = 1.0,
                                        device_token = 'test',
                                        username = 'jenkins',
                                        uuid = 'uuid')
        device_token.save()
        saved_device_token = DeviceTokenModel.objects.all()
        self.assertEqual(saved_device_token.count(), 1)

        token = saved_device_token[0]
        self.assertEqual(token.os_version, 1.0)
        self.assertEqual(token.device_token, 'test')
        self.assertEqual(token.username, 'jenkins')
        self.assertEqual(token.uuid, 'uuid')

class NotificationModelTest(TestCase):
    def test_is_empty(self):
        saved_notification = NotificationModel.objects.all()
        self.assertEqual(saved_notification.count(), 0)

    def test_is_not_empty(self):
        create_notification = NotificationModel(os_version = 1.0,
                                         username = 'jenkins',
                                         badge = 1,
                                         execute_datetime = '2016/11/08 01:17')
        create_notification.save()
        saved_notification = NotificationModel.objects.all()
        self.assertEqual(saved_notification.count(), 1)

        one_notification = saved_notification[0]
        self.assertEqual(one_notification.title, '')
        self.assertEqual(one_notification.message, '')
        self.assertEqual(one_notification.os_version, 1.0)
        self.assertEqual(one_notification.sound, '')
        self.assertEqual(one_notification.badge, 1)
        self.assertEqual(one_notification.url, '')
        self.assertEqual(one_notification.json, '')
        self.assertEqual(one_notification.content_available, False)
        self.assertEqual(one_notification.is_production, False)
        self.assertEqual(one_notification.username, 'jenkins')
        self.assertEqual(one_notification.is_sent, False)

class DevelopFileModelTest(TestCase):
    def test_is_empty(self):
        saved_develop = DevelopFileModel.objects.all()
        self.assertEqual(saved_develop.count(), 0)

    def test_is_not_empty(self):
        one_develop = DevelopFileModel(upload_username = 'jenkins',
                                       development_file_name = 'test/develop.pem')
        one_develop.save()
        saved_develop = DevelopFileModel.objects.all()
        develop = saved_develop[0]
        self.assertEqual(develop.upload_username, 'jenkins')
        self.assertEqual(develop.development_file_name, 'test/develop.pem')

class ProductFileModelTest(TestCase):
    def test_is_empty(self):
        saved_product = ProductFileModel.objects.all()
        self.assertEqual(saved_product.count(), 0)

    def test_is_not_empty(self):
        one_product = ProductFileModel(upload_username = 'jenkins',
                                       production_file_name = 'test/product.pem')
        one_product.save()
        saved_product = ProductFileModel.objects.all()
        product = saved_product[0]
        self.assertEqual(product.upload_username, 'jenkins')
        self.assertEqual(product.production_file_name, 'test/product.pem')
