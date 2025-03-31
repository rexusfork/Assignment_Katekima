from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime
from weasyprint import HTML

from items.models import Item
from purchases.models import PurchaseDetail
from sells.models import SellDetail


# Create your views here.
class StockReportView(APIView):
    def get(self, request, item_code):
        # Mengambil query untuk start_date dan end_date
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        # Mengecek Query Params (Mandatory)
        if not (start_date and end_date):
            return Response(
                {"error": "start_date and end_date are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Cek format untuk start_date dan end_date
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mencari Item berdasarkan item_code dan belum pernah di delete.
        item = get_object_or_404(Item, code=item_code, is_deleted=False)

        # Ambil Pembelian dalam rentang waktu dari parameter start_date dan end_date
        purchases = PurchaseDetail.objects.filter(
            item_code=item,
            header_code__date__range=(start_date_obj, end_date_obj),
            header_code__is_deleted=False,
        ).select_related("header_code")

        # Ambil Penjualan dalam rentang waktu dari parameter start_date dan end_date
        sells = SellDetail.objects.filter(
            item_code=item,
            header_code__date__range=(start_date_obj, end_date_obj),
            header_code__is_deleted=False,
        ).select_related("header_code")

        # Tempat Penyimpanan transaksi akhir yang ditampilkan kepada user
        history = []

        # Menyimpan batch stock dalam bentuk [qty, price]
        stock_layers = []

        # Total Barang yang masuk dan keluar
        total_in = 0
        total_out = 0

        # Menggabungkan dan mengurutkan transaksi
        transactions = []

        # Menambahkan transaksi untuk type Pembelian
        for p in purchases:
            transactions.append(
                {
                    "type": "purchase",
                    "date": p.header_code.date,
                    "description": p.header_code.description,
                    "code": p.header_code.code,
                    "qty": p.quantity,
                    "price": p.unit_price,
                }
            )

        # Menambahkan transaksi untuk type Penjualan
        for s in sells:
            transactions.append(
                {
                    "type": "sell",
                    "date": s.header_code.date,
                    "description": s.header_code.description,
                    "code": s.header_code.code,
                    "qty": s.quantity,
                }
            )

        # Mengurutkan transaksi berdasarkan tanggal
        transactions.sort(key=lambda x: x["date"])

        # Menggabungkan transaksi pembelian dan penjualan
        # Menggunakan Konsep First In First Out (FIFO)
        for transaction in transactions:

            # Jika Transaksi merupakan pembelian
            if transaction["type"] == "purchase":
                qty = transaction["qty"]
                price = transaction["price"]

                # Menambahkan batch baru ke stock_layers
                stock_layers.append([qty, price])

                # Jumlah Total Masuk untuk Summary
                total_in += qty

                # jumlah barang dari setiap batch
                stock_qty = [layer[0] for layer in stock_layers]

                # harga dari setiap batch
                stock_price = [layer[1] for layer in stock_layers]

                # Total harga dari tiap batch
                stock_total = [
                    qty * price for qty, price in zip(stock_qty, stock_price)
                ]

                history.append(
                    {
                        "date": transaction["date"],
                        "description": transaction["description"],
                        "code": transaction["code"],
                        "in_qty": qty,
                        "in_price": price,
                        "in_total": qty * price,
                        "out_qty": 0,
                        "out_price": 0,
                        "out_total": 0,
                        "stock_qty": stock_qty,
                        "stock_price": stock_price,
                        "stock_total": stock_total,
                        "balance_qty": sum(stock_qty),
                        "balance_total": sum(stock_total),
                    }
                )

            # Jika Transaksi merupakan penjualan
            else:
                qty = transaction["qty"]

                # Total Keluar untuk Summary
                out_total = 0

                # Mencatat batch yang digunakan untuk penjualan
                used_batches = []

                # Looping setiap batch dimulai dari yang paling bawah
                for layer in stock_layers:
                    if qty <= 0:
                        break

                    # Jumlah barang yang tersedia pada batch ini
                    available = layer[0]

                    # Harga dari batch ini
                    price = layer[1]

                    #  Lewati jika batch sudah habis
                    if available == 0:
                        continue

                    # Mengambil sebanyak mungkin dari batch ini sesuai dengan qty yang diperlukan
                    take = min(available, qty)

                    # Mengurangi stock batch
                    layer[0] -= take

                    # Mengurangi qty yang diperlukan
                    qty -= take

                    out_total += take * price

                    # Mencatat berapa banyak yang diambil dari batch ini
                    used_batches.append((take, price))

                # Total keluar untuk summary
                total_out += transaction["qty"] - qty

                # Mengambil harga dari batch pertama yang dipakai
                first_batch_price = used_batches[0][1] if used_batches else 0

                # Update Kondisi stock setelah penjualan
                stock_qty = [layer[0] for layer in stock_layers]
                stock_price = [
                    layer[1] if layer[0] > 0 else 0 for layer in stock_layers
                ]
                stock_total = [q * p for q, p in zip(stock_qty, stock_price)]

                history.append(
                    {
                        "date": transaction["date"],
                        "description": transaction["description"],
                        "code": transaction["code"],
                        "in_qty": 0,
                        "in_price": 0,
                        "in_total": 0,
                        "out_qty": transaction["qty"],
                        "out_price": first_batch_price,
                        "out_total": out_total,
                        "stock_qty": stock_qty,
                        "stock_price": stock_price,
                        "stock_total": stock_total,
                        "balance_qty": sum(stock_qty),
                        "balance_total": sum(stock_total),
                    }
                )

        context = {
            "items": history,
            "item_code": item_code,
            "name": item.name,
            "unit": item.unit,
            "summary": {
                "total_in": total_in,
                "total_out": total_out,
                "stock": sum([layer[0] for layer in stock_layers]),
                "balance": sum([layer[0] for layer in stock_layers]),
            },
        }

        # Render dari HTML menjadi String
        html_string = render_to_string("stock_report.html", context)

        # Render string HTML ke PDF
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="stock_report_{item_code}.pdf"'
        )

        # Menggunakan WeasyPrint untuk mengenerate dari String yang diubah dari HTML
        HTML(string=html_string).write_pdf(response)

        # Return dalam bentuk PDF
        return response
