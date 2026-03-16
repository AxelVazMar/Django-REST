from django.test import TestCase
from api.models import Order, User, Product
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)
    
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username='user2')
        self.client.force_login(user)
        response = self.client.get(reverse('order-list'))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order['user'] == user.id for order in orders))

    def test_user_order_list_aunauthenticated(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass123')
        self.normal_user = User.objects.create_user(username='user', password='userpass123')
        self.product = Product.objects.create(
            name = 'Test Product',
            description = 'This is a test product',
            price = 9.99,
            stock = 10
        )
        self.url = reverse('product-detail', kwargs={'id': self.product.pk})

    def test_get_product(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_unauthorized_update_product(self):
        data = {'name': 'Updated Name'}
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_only_admins_can_delete_product(self):
        # test normal user cannor delete - nore that this could be its own method
        self.client.login(username='user', password='userpass123')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists()) # We expect the product exists because the normal user should not be able to delete it

        # test admin user can delete
        self.client.login(username='admin', password='adminpass123')
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists()) # We expect the product does not exist because the admin user should be able to delete it

    def test_only_admins_can_update_product(self):
        # Put
        self.client.login(username='admin', password='adminpass123')
        data = {
            'name': 'New product name',
            'description': 'New description',
            'price': 19.99,
            'stock': 5
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Patch
        data = {'name': 'Partially updated name'}
        response = self.client.patch(self.url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
