from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "sheets"
urlpatterns = [
    path("", views.index, name="index"),
    #  Sheets
    path(
        "<int:year>/<int:month>/",
        views.SheetView.as_view(month_format="%m"),
        name="sheet",
    ),
    path("expense/new/", views.ExpenseCreateView.as_view(), name="expense-new"),
    path(
        "expense/<int:pk>/",
        views.ExpenseUpdateView.as_view(),
        name="expense-edit",
    ),
    path(
        "expense/<int:pk>/delete/",
        views.ExpenseDeleteView.as_view(),
        name="expense-delete",
    ),
    #  History
    path("expense/history/", views.ExpenseListView.as_view(), name="history"),
    #  Categories
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path(
        "category/new/", views.CategoryCreateView.as_view(), name="category-new"
    ),
    path(
        "category/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="category-edit",
    ),
    path(
        "category/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    #  Banks
    path("banks/", views.BanksListView.as_view(), name="banks"),
    path(
        "banks/new/", views.BanksCreateView.as_view(), name="banks-new"
    ),
    
    path(
        "banks/<int:pk>/",
        views.BanksUpdateView.as_view(),
        name="banks-edit",
    ),
    path(
        "banks/<int:pk>/delete/",
        views.BanksDeleteView.as_view(),
        name="banks-delete",
    ),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
