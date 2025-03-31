from django.urls import path
from .views import SellHeaderGetListCreateView, SellDetailView, SellHeaderGetByCodeEditDeleteView

urlpatterns = [
    path('', SellHeaderGetListCreateView.as_view(), name='sell-header-list-create'),
    path('<str:code>/', SellHeaderGetByCodeEditDeleteView.as_view(), name='sell-header-update-delete-get'),
    path('<str:header_code>/details', SellDetailView.as_view(), name='sell-detail-get-post'),
]
