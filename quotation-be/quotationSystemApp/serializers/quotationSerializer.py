import json
from rest_framework import serializers
from quotationSystemApp.models.quotation import Quotation, Item
from quotationSystemApp.models.itemsQuotation import ItemsQuotation


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = [ 'client', 'iva', 'discount', 'observation']
    def to_representation(self, obj):
        quotation = Quotation.objects.get(id=obj.id)
        itemsQuotation = ItemsQuotation.objects.filter(quotation_id=quotation.id)
        return {
            'id': quotation.id,
            'client': quotation.client.id,
            'client_name': quotation.client.name,
            'client_city': quotation.client.city,
            'client_address': quotation.client.address,
            'client_email': quotation.client.email,
            'client_phone': quotation.client.phone,
            'date': quotation.dateTime.date().strftime('%d/%m/%Y'),
            'time': quotation.dateTime.time().strftime('%H:%M'),
            'iva': quotation.iva,
            'discount': quotation.discount,
            'subtotal': quotation.subtotal,
            'totalDiscount': quotation.totalDiscount,
            'totalIva': quotation.totalIva,
            'total': quotation.total,
            'quotationItems': itemsQuotation.values(),
            'observation': quotation.observation
        }