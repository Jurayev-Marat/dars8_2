from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.views import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import *
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import viewsets, permissions
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum, Count, F


class EmployeeStatisticsAPIView(APIView):
    def get(self, request):
        data = (
            Order.objects
            .values('employee__full_name')
            .annotate(
                orders_count=Count('id'),
                total_items=Sum('items__quantity')
            )
        )
        return Response(data)

        data = (
            orders.values('employee__full_name').annotate(
                total_sales=Sum('items_quantity'),
                total_amount=Sum('items__quantity' * F('items__product__price')),
                unique_clients=Count('cilent', distinct=True)
            )
        )
        return Response(data)


class ClientStatisticsAPIView(APIView):
    def get(self, request, id):
        month = request.GET.get('month')
        year = request.GET.get('year')

        orders = Order.objects.filter(
            client_id=id,
            created_at__month=month,
            created_at__year=year
        )

        total_amount = sum(i.total_price for i in orders)

        product = OrderItem.objects.filter(order__in=orders).values(
            'product__name'
        ).annotate(total_quantity=Sum('quantity'))

        return Response({
            'client_id': id,
            'total_amount': total_amount,
            'product': product
        })