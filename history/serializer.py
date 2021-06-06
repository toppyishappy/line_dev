from datetime import datetime
from rest_framework import serializers

from history.models import ReservartionHistory


class ReserveListSerialize(serializers.ModelSerializer):
    reserved_date = serializers.SerializerMethodField()
    class Meta:
        model = ReservartionHistory
        fields = ['user_name', 'location', 'reserved_date', 'is_paid', 'id']

    def get_reserved_date(self, obj):
        return datetime.strftime(obj.reserved_date, '%d/%m/%Y')

    def update(self, instance, validated_data):
        instance.is_paid = validated_data.get('is_paid', instance.is_paid)
        instance.booker = validated_data.get('booker', instance.booker)
        
        return instance.save()