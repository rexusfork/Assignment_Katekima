from django.urls import path
from .views import StockReportView

urlpatterns = [
    path("<str:item_code>/", StockReportView.as_view(), name="stock-report"),
]
