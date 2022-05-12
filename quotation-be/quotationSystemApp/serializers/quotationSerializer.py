from rest_framework import serializers
from quotationSystemApp.models.quotation import Quotation, Item


class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['id', 'item', 'quantity', 'price', 'total', 'client', 'date', 'time', 'iva', 'discount']
    def to_representation(self, obj):
        quotation = Quotation.objects.get(id=obj.id)
        return {
            'id': quotation.id,
            'item': quotation.item.name,
            'quantity': quotation.quantity,
            'price': quotation.price,
            'total': quotation.total,
            'client': quotation.client.name,
            'date': quotation.date.strftime("%d/%m/%Y"),
            'time': quotation.time.strftime("%H:%M"),
            'iva': quotation.iva,
            'discount': quotation.discount
        }