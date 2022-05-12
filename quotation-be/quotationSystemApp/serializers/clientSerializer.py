from rest_framework import serializers
from quotationSystemApp.models.client import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'city', 'address', 'email', 'phone']
    def to_representation(self, obj):
        client = Client.objects.get(id=obj.id)
        return {
            'id': client.id,
            'name': client.name,
            'city': client.city,
            'address': client.address,
            'email': client.email,
            'phone': client.phone
        }