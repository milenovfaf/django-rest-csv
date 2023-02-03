import codecs
import csv
from django.db.models import Count, Sum, Case, When
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Deals
from .serializers import InputDealsSerializer
from django.contrib.postgres.aggregates import ArrayAgg

from django.urls import path
from django.http import JsonResponse
from django.core.cache import cache
import datetime


class DealsAPIView(APIView):
    CACHE_KEY = 'top_five_spending_clients'

    def _top_five_spending_clients(self):
        top_five_customers = (Deals.objects
                              .values('customer')
                              .annotate(spent_money=Sum('total'))
                              .order_by('-spent_money')[:5])
        gems = (Deals.objects
                    .filter(customer__in=top_five_customers.values_list('customer', flat=True))
                    .values('customer', 'gem')
                    .annotate(count_gems=Count('gem'))
                    .order_by('customer', 'gem'))
        gems_stat = {}
        _last_customer = None
        for item in gems:
            gem = item['gem']
            if gem not in gems_stat:
                gems_stat[gem] = 0
            #
            gems_stat[gem] += 1
        #
        clients_gems = {}
        for item in gems:
            username = item['customer']
            if username not in clients_gems:
                clients_gems[username] = []
            #
            gem = item['gem']
            if gems_stat[gem] >= 2:
                clients_gems[username].append(
                    gem
                )
            #
        #
        result = []
        for customer in top_five_customers:
            result.append({
                'username':     customer['customer'],
                'spent_money':  customer['spent_money'],
                'gams':         clients_gems.get(customer['customer'], []),
            })
        #
        return Response({
            'response': result,
        })

    def get(self, request):
        data = cache.get('CACHE_KEY')
        if not data:
            data = self._top_five_spending_clients()
            cache.set('CACHE_KEY', data, 60 * 5)
            return Response(data)
        #
        return JsonResponse(data)

    def post(self, request, cache_key):
        file_obj = request.FILES['file']
        if not file_obj.name.endswith('.csv'):
            return Response({
                'Desc': 'File is not CSV'
            }, status=status.HTTP_400_BAD_REQUEST)
        #
        _result_objects = []
        reader = csv.DictReader(codecs.iterdecode(file_obj, 'utf-8'))
        for i, row in enumerate(reader):
            serializer = InputDealsSerializer(data=row)
            if not serializer.is_valid():
                return Response({
                    'Desc':     f'invalid data format at line {i}',
                    'errors':   serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)
            #
            row_data = dict(serializer.validated_data)
            row_data['gem'] = row_data.pop('item')
            _result_objects.append(
                Deals(
                    **row_data,
                )
            )
        #
        cache.delete_pattern(cache_key)
        Deals.objects.all().delete()
        Deals.objects.bulk_create(_result_objects)

        return Response({
            'success': f'Deals uploaded successfully {len(_result_objects)} lines'
        }, status=status.HTTP_200_OK)

