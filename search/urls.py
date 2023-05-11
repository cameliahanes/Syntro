from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name="search"),
    path('redirect/<int:paper_id>', views.redirect, name="redirect")
]
