from rest_framework import serializers
from quotationSystemApp.models.item import Item
from quotationSystemApp.models.itemsQuotation import ItemsQuotation


class ItemsQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsQuotation
        fields = ['id', 'price','name', 'quotation', 'item', 'quantity', 'total']
    def to_representation(self, obj):
        itemsQuotation = ItemsQuotation.objects.get(id=obj.id)
        return {
            'id': itemsQuotation.id,
            'quotationId': itemsQuotation.quotation.id,
            'itemId': itemsQuotation.item.id,
            'name': itemsQuotation.item.name,
            'price': itemsQuotation.item.price,
            'quantity': itemsQuotation.quantity,
            'total': itemsQuotation.total,
        }