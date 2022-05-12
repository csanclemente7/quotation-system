from rest_framework import serializers
from quotationSystemApp.models.item import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'price']
    def to_representation(self, obj):
        item = Item.objects.get(id=obj.id)
        return {
            'id': item.id,
            'name': item.name,
            'price': item.price
        }