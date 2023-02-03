from rest_framework import serializers


class InputDealsSerializer(serializers.Serializer):
    customer = serializers.CharField(max_length=255)
    item = serializers.CharField(max_length=255)
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)
    date = serializers.DateTimeField(input_formats=[
        '%Y-%m-%d %H:%M:%S.%f',
    ])
