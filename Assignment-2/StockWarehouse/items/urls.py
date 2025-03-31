from django.urls import path
from .views import ItemGetEditDeleteView, ItemListCreateView

urlpatterns = [
    path("", ItemListCreateView.as_view(), name="item-list-create"),
    path("<str:code>/", ItemGetEditDeleteView.as_view(), name="item-update-delete-get"),
]
