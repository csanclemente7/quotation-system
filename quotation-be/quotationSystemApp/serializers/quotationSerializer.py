from rest_framework import serializers
from quotationSystemApp.models.quotation import Quotation, Item


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = [ 'client', 'iva', 'discount']
    def to_representation(self, obj):
        quotation = Quotation.objects.get(id=obj.id)
        return {
            'id': quotation.id,
            'client': quotation.client.name,
            'date': quotation.dateTime.date().strftime('%d/%m/%Y'),
            'time': quotation.dateTime.time().strftime('%H:%M'),
            'iva': quotation.iva,
            'discount': quotation.discount,
            'subtotal': quotation.subtotal,
            'totalDiscount': quotation.totalDiscount,
            'totalIva': quotation.totalIva,
            'total': quotation.total,
        }