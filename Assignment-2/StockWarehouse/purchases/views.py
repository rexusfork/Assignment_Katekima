from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    PurchaseHeaderBaseSerializer,
    PurchaseHeaderUpdateSerializer,
    PurchaseDetailBaseSerializer,
)
from .models import PurchaseHeader, PurchaseDetail

PURCHASE_NOT_FOUND_MESSAGE = "Item not found"


# Create your views here.
class PurchaseHeaderGetEditDeleteView(APIView):
    serializer_base_class = PurchaseHeaderBaseSerializer

    # Logika: Mengambil Purchase berdasarkan code
    def get(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            purchase_header = PurchaseHeader.objects.get(code=code, is_deleted=False)

            # DTO: PurchaseHeader ke PurchaseHeaderBase
            serializer = PurchaseHeaderBaseSerializer(purchase_header)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        # Purchase Header Tidak Ada
        except PurchaseHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": PURCHASE_NOT_FOUND_MESSAGE},
            )

    def put(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            purchase_header = PurchaseHeader.objects.get(code=code, is_deleted=False)

            # DTO: Request ke Purchase Header Update (Khusus bagian yang diubah saja)
            serializer = PurchaseHeaderUpdateSerializer(
                purchase_header, data=request.data
            )

            if serializer.is_valid():
                # Menyimpan perubahan kedalam database
                serializer.save()
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        # Purchase Header Tidak Ada
        except PurchaseHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": PURCHASE_NOT_FOUND_MESSAGE},
            )

    def delete(self, request, code):
        try:
            # Mencari berdasarkan code dan belum pernah dihapus
            purchase_header = PurchaseHeader.objects.get(code=code, is_deleted=False)

            # Mengubah status deleted
            purchase_header.is_deleted = True

            # Menyimpan perubahan kedalam database
            purchase_header.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Purchase Header Tidak Ada
        except PurchaseHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": PURCHASE_NOT_FOUND_MESSAGE},
            )


class PurchaseHeaderCreateListView(APIView):
    # DTO: Base
    serializer_base_class = PurchaseHeaderBaseSerializer

    # Logika: Mengambil Semua Purchase Header
    def get(self, request):
        # Mengambil Semua Purchase Header yang belum pernah dihapus
        purchases = PurchaseHeader.objects.filter(is_deleted=False)

        # List Kosong
        if not purchases:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": PURCHASE_NOT_FOUND_MESSAGE},
            )

        # DTO: Purchase Header ke Purchase Header Base
        serializer = PurchaseHeaderBaseSerializer(purchases, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # Logika: Menambahkan Purchase Header Baru
    def post(self, request):
        serializer = self.serializer_base_class(data=request.data)

        if serializer.is_valid():
            # Menyimpan ke dalam Database
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class PurchaseDetailView(APIView):
    # Logika: Mengambil Semua Purchase
    def get(self, request, header_code):
        try:
            # Mengambil Semua Purchase berdasarkan header_code dan belum pernah dihapus
            purchase_detail = PurchaseDetail.objects.filter(
                header_code=header_code, is_deleted=False
            )

            # DTO: Purchase Detail ke Purchase Detail Base
            serializer = PurchaseDetailBaseSerializer(purchase_detail, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)

        # Jika Tidak ada Purchase Detail
        except PurchaseDetail.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": PURCHASE_NOT_FOUND_MESSAGE},
            )

    # Logika: Membuat Purchase Detail
    def post(self, request, header_code):
        try:
            # Cek Header Code
            purchase_header = PurchaseHeader.objects.get(
                code=header_code, is_deleted=False
            )

            # DTO: Request ke Purchase
            serializer = PurchaseDetailBaseSerializer(data=request.data)

            if serializer.is_valid():
                # Menyimpan Data dari Request dan Menambahkan header_code
                serializer.save(header_code=purchase_header)
                return Response(status=status.HTTP_201_CREATED, data=serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        # Jika Header_code tidak ada.
        except PurchaseHeader.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": PURCHASE_NOT_FOUND_MESSAGE},
            )