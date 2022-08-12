from django.urls import path

from .views.keys import KeyView, KeyCreateView, KeyEditView, KeyUseView
from .views.datatables.keys import KeyDataView


app_name = "frontend"

urlpatterns = [
    path("", KeyView.as_view(), name="keys"),
    path("data/", KeyDataView.as_view(), name="key_list_data"),
    path("add/", KeyCreateView.as_view(), name="create_key"),
    path("<int:pk>/edit/", KeyEditView.as_view(), name="edit_key"),
    path("<int:pk>/use/", KeyUseView.as_view(), name="use_key"),
]