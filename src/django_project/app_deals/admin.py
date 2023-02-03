from django.contrib import admin
from .models import Deals


@admin.register(Deals)
class Deals(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'customer',
        'gem',
        'quantity',
        'total',
    )
    list_filter = (
        'date',
    )
    search_fields = (
        'customer',
        'gem',
    )
