from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Accounts


User = get_user_model()


class AccountsListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password',
        )
        self.client.force_authenticate(user=self.user)
        self.account1 = Accounts.objects.create(
            user=self.user,
            service_name='Service1',
            email='test1@test.com',
            password='pass1',
        )
        self.account2 = Accounts.objects.create(
            user=self.user,
            service_name='Service2',
            email='test2@test.com',
            password='pass2',
        )

    def test_get_accounts_list(self):
        url = reverse('accounts-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_by_service_name(self):
        url = reverse('accounts-list-create')
        response = self.client.get(url, {'service_name': 'Service1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['service_name'], 'Service1')

    def test_filter_by_email(self):
        url = reverse('accounts-list-create')
        response = self.client.get(url, {'email': 'test1@test.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['email'], 'test1@test.com')

    def test_ordering(self):
        url = reverse('accounts-list-create')
        response = self.client.get(url, {'ordering': '-service_name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['service_name'], 'Service2')

    def test_create_account(self):
        url = reverse('accounts-list-create')
        data = {'service_name': 'Service3', 'email': 'test3@test.com', 'password': 'pass3'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Accounts.objects.count(), 3)
        self.assertEqual(Accounts.objects.last().user, self.user)


class AccountsDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password',
        )
        self.other_user = User.objects.create_user(
            username='other_user',
            password='other_password',
        )
        self.client.force_authenticate(user=self.user)
        self.account = Accounts.objects.create(
            user=self.user,
            service_name='Service1',
            email='test1@test.com',
            password='pass1',
        )

    def test_get_account_detail(self):
        url = reverse('accounts-detail', kwargs={'pk': self.account.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['service_name'], 'Service1')

    def test_get_other_user_account_detail(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('accounts-detail', kwargs={'pk': self.account.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_account(self):
        url = reverse('accounts-detail', kwargs={'pk': self.account.pk})
        data = {
            'service_name': 'UpdatedService',
            'email': 'updated@test.com',
            'password': 'updatedpass'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.service_name, 'UpdatedService')

    def test_delete_account(self):
        url = reverse('accounts-detail', kwargs={'pk': self.account.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Accounts.objects.count(), 0)


class DecryptPasswordViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password',
        )
        self.client.force_authenticate(user=self.user)
        self.account = Accounts.objects.create(
            user=self.user,
            service_name='Service1',
            email='test1@test.com',
            password='encryptedpass',
        )

    def test_decrypt_password(self):
        url = reverse('decrypt-password', kwargs={'pk': self.account.pk})
        data = {'master_password': 'test_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('decrypted_password', response.data)

    def test_decrypt_password_wrong_master_password(self):
        url = reverse('decrypt-password', kwargs={'pk': self.account.pk})
        data = {'master_password': 'wrongmasterpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_decrypt_password_other_user_account(self):
        other_user = User.objects.create_user(
            username='other_user',
            password='other_password',
        )
        self.client.force_authenticate(user=other_user)
        url = reverse('decrypt-password', kwargs={'pk': self.account.pk})
        data = {'master_password': 'masterpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
