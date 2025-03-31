from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SellHeader, SellDetail
from .serializers import (
    SellHeaderBaseSerializer,
    SellHeaderUpdateSerializer,
    SellDetailBaseSerializer,
)

SELL_NOT_FOUND_MESSAGE = "Sell not found"


# Create your views here.
class SellHeaderGetListCreateView(APIView):
    def get(self, request):
        # Mengambil Semua Sell Header yang belum pernah di hapus
        sells = SellHeader.objects.filter(is_deleted=False)

        # List Kosong
        if not sells:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": SELL_NOT_FOUND_MESSAGE},
            )

        serializer = SellHeaderBaseSerializer(sells, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def post(self, request):
        # DTO: Request ke Sell Header Base
        serializer = SellHeaderBaseSerializer(data=request.data)

        if serializer.is_valid():
            # Menyimpan perubahan kedalam database
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class SellHeaderGetByCodeEditDeleteView(APIView):
    def get(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            sell_header = SellHeader.objects.get(code=code, is_deleted=False)

            # DTO: Sell Header ke Sell Header Base
            serializer = SellHeaderBaseSerializer(sell_header)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        # Jika Tidak ada Sell Header
        except SellHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": SELL_NOT_FOUND_MESSAGE},
            )

    def put(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            sell_header = SellHeader.objects.get(code=code, is_deleted=False)

            # DTO: Sell Header ke Sell Header Base
            serializer = SellHeaderUpdateSerializer(sell_header, data=request.data)

            if serializer.is_valid():
                # Menyimpan perubahan kedalam database
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        # Jika Tidak ada Sell Header
        except SellHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": SELL_NOT_FOUND_MESSAGE},
            )

    def delete(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            sell_header = SellHeader.objects.get(code=code, is_deleted=False)

            # Mengubah status deleted
            sell_header.is_deleted = True

            # Menyimpan perubahan kedalam database
            sell_header.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Jika Tidak ada Sell Header
        except SellHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": SELL_NOT_FOUND_MESSAGE},
            )


class SellDetailView(APIView):
    # Logika: Mengambil Semua Detail Sell berdasarkan header_code dan tidak pernah dihapus sebelumnya
    def get(self, request, header_code):
        try:
            # Mengambil Semua Sell berdasarkan header code dan belum pernah dihapus
            sell_detail = SellDetail.objects.filter(
                header_code=header_code, is_deleted=False
            )

            # DTO: Sell Detail ke Sell Detail Base
            serializer = SellDetailBaseSerializer(sell_detail, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        # Jika Tidak ada Sell Detail
        except SellDetail.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": SELL_NOT_FOUND_MESSAGE},
            )

    # Logika: Membuat Sell Detail baru
    def post(self, request, header_code):
        try:
            # Cek Header Code
            sell_header = SellHeader.objects.get(header_code=header_code, is_deleted=False)

            # DTO: Request ke Purchase
            serializer = SellDetailBaseSerializer(data=request.data)

            if serializer.is_valid():
                # Menyimpan Perubahan ke dalam Database
                serializer.save(header_code=sell_header)
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        # Jika Header Code tidak ada
        except SellHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": SELL_NOT_FOUND_MESSAGE},
            )
