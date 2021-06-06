from rest_framework import serializers

from accounts.models import User



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['line', 'username', 'phone_number', 'password', 'role']

    def validate_phone_number(self, phone):
        if not len(phone) == 10 and not phone.startswith('0'):
            raise serializers.ValidationError("incorrect phone number")

    def create(self, validate):
        phone = validate.get('phone_number')
        return User.objects.create(**validate)


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'