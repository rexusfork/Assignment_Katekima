from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemBaseSerializer, UpdateItemSerializer

ITEM_NOT_FOUND_MESSAGE = "Item not found"


# Create your views here.
class ItemGetEditDeleteView(APIView):
    # Logika: Mengambil Item berdasarkan code
    def get(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            item = Item.objects.get(code=code, is_deleted=False)

            serializer = ItemBaseSerializer(item)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        # Jika Code tidak ada, maka mengembalikan pesan error
        except Item.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": ITEM_NOT_FOUND_MESSAGE},
            )

    # Logika: Edit dibagian Items
    def put(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            item = Item.objects.get(code=code, is_deleted=False)

            # DTO: request ke Item (Khusus bagian yang diubah saja)
            serializer = UpdateItemSerializer(item, data=request.data)

            if serializer.is_valid():
                # Menyimpan perubahan kedalam database
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        except Item.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": ITEM_NOT_FOUND_MESSAGE},
            )

    # Logika: Soft Delete untuk Item
    def delete(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            item = Item.objects.get(code=code, is_deleted=False)

            # Mengubah status deleted
            item.is_deleted = True

            # Menyimpan perubahan kedalam database
            item.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Item.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": ITEM_NOT_FOUND_MESSAGE},
            )


class ItemListCreateView(APIView):
    # Logika: Mengambil Semua Item
    def get(self, request):
        # Mengambil semua Item yang belum pernah dihapus
        items = Item.objects.filter(is_deleted=False)

        # List Kosong
        if not items:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": ITEM_NOT_FOUND_MESSAGE},
            )

        # DTO: Item ke GetListItem Response
        serializazer = ItemBaseSerializer(items, many=True)
        return Response(status=status.HTTP_200_OK, data=serializazer.data)

    # Logika: Membuat Item baru
    def post(self, request):
        # DTO: Request ke ItemBase
        serializer = ItemBaseSerializer(data=request.data)

        if serializer.is_valid():
            # Menyimpan Data dari Request
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
