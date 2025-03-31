from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Item
from .serializers import ItemBaseSerializer, GetListItemSerializer, UpdateItemSerializer


# Create your tests here.
class ItemAPITestCase(APITestCase):
    def setUp(self):
        self.item = Item.objects.create(
            code="ABC123",
            name="Test Item",
            description="Item description",
            is_deleted=False,
        )
        self.create_url = reverse("item-list-create")
        self.detail_url = reverse("item-update-delete-get", args=[self.item.code])

    def test_get_item_by_code_success(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["code"], self.item.code)

    def test_get_item_by_code_not_found(self):
        url = reverse("item-get-edit-delete", args=["NOTEXIST"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_update_item_success(self):
        data = {"name": "Updated Name", "description": "Updated description"}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, data["name"])

    def test_put_update_item_not_found(self):
        url = reverse("item-get-edit-delete", args=["INVALID"])
        response = self.client.put(url, {"name": "New"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_success(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.item.refresh_from_db()
        self.assertTrue(self.item.is_deleted)

    def test_delete_item_not_found(self):
        url = reverse("item-get-edit-delete", args=["INVALID"])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_item_list_success(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_item_list_empty(self):
        self.item.is_deleted = True
        self.item.save()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_create_item_success(self):
        data = {
            "code": "XYZ999",
            "name": "New Item",
            "description": "New item description",
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Item.objects.filter(code="XYZ999").exists())

    def test_post_create_item_invalid(self):
        data = {"code": "", "name": "", "description": ""}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
