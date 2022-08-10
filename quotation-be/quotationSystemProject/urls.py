"""quotationSystemProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView)
from quotationSystemApp import views


urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('register', views.UserCreateView.as_view()),

    # URLS de usuario
    path('user/<int:pk>', views.UserDetailView.as_view()),

    # URLS de item
    path('item/<int:user>', views.ItemCreateView.as_view()), #ok
    path('item/<int:user>/<int:pk>', views.ItemDetailView.as_view()), #ok
    path('items/<int:user>', views.ItemListView.as_view()), #ok
    path('item/<int:user>/<int:pk>/update', views.ItemUpdateView.as_view()), #ok
    path('item/<int:user>/<int:pk>/delete', views.ItemDeleteView.as_view()), #ok

    # URLS de cliente
    path('client/<int:user>', views.ClientCreateView.as_view()), #ok
    path('client/<int:user>/<int:pk>', views.ClientDetailView.as_view()), #ok
    path('clients/<int:user>', views.ClientListView.as_view()), #ok

    # URLS de cotización
    path('quotation/<int:user>', views.QuotationCreateView.as_view()), #ok
    path('quotation/<int:user>/<int:pk>', views.QuotationDetailView.as_view()), #ok
    path('quotations/<int:user>', views.QuotationListView.as_view()), #ok
    path('quotation/<int:user>/<int:pk>/update', views.QuotationUpdateView.as_view()),
    path('quotation/<int:user>/<int:pk>/delete', views.QuotationDeleteView.as_view()),

    # URLS de items de cotización
    path('itemsQuotation/<int:user>', views.ItemsQuotationCreateView.as_view()),
    path('itemsQuotation/<int:user>/<int:pk>', views.ItemsQuotationUpdateView.as_view()),
    path('itemsQuotation/<int:user>/<int:pk>/delete', views.ItemsQuotationDeleteView.as_view()),
    path('itemsQuotation/<int:user>/list', views.ItemsQuotationListView.as_view()),
    path('itemsQuotation/<int:user>/<int:pk>/list', views.ItemsQuotationByQuotationListView.as_view()),

    # URL billing Statement

    path('billingStatement/<int:user>', views.BillingStatementCreateView.as_view()), #ok
    path('billingStatement/<int:user>/<int:pk>/delete', views.BillingStatementDeleteView.as_view()),
    path('billingStatement/<int:user>/list', views.BillingStatementListView.as_view()),
    path('billingStatement/<int:user>/<int:pk>', views.BillingStatementDetailView.as_view()), #ok

]
