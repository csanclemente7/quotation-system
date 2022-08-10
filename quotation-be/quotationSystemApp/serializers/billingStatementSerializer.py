import json
from rest_framework import serializers
from quotationSystemApp.models.billingStatement import BillingStatement


class BillingStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingStatement
        fields = [ 'id', 'quotation']
