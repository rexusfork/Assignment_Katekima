from django.urls import path
from .views import PurchaseHeaderGetEditDeleteView, PurchaseDetailView, PurchaseHeaderCreateListView

urlpatterns = [
    path('', PurchaseHeaderCreateListView.as_view(), name='item-list-create'),
    path('<str:code>/', PurchaseHeaderGetEditDeleteView.as_view(), name='item-update-delete-get'),
    path('<str:header_code>/details/', PurchaseDetailView.as_view(), name='purchase-get-create'),
]
