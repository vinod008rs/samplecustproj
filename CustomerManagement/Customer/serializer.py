import datetime, re
from rest_framework import serializers
from .models import CustomerModel
from .utils import calculate_age
from phonenumber_field.serializerfields import PhoneNumberField


class CustomerSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False, )
    firstName = serializers.CharField(source='first_name', required=True, max_length=256)
    lastName = serializers.CharField(source='last_name', required=True, max_length=256)
    dateOfBirth = serializers.CharField(source='date_of_birth', required=True, max_length=20)
    phoneNumber = PhoneNumberField(source='phone_number', required=True, max_length=20)

    class Meta:
        model = CustomerModel
        fields = ['id', 'firstName', 'lastName', 'dateOfBirth', 'phoneNumber']

    def validate_phone_number(self, value):
        # Validate phone number format (E.164)
        phone_regex = r'^\+[1-9]\d{1,14}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError('Invalid phone number format. Use E.164 format')
        return value
    def validate(self, attrs):
        errors = {}
        # Validate date_of_birth
        date_of_birth = datetime.datetime.strptime(attrs.get('date_of_birth'), '%Y-%m-%d')

        # Additional custom validations
        # Example: Validate age based on date_of_birth
        # Note: You may need to adjust this logic based on your requirements
        if date_of_birth:
            age = calculate_age(date_of_birth)  # Custom function to calculate age
            if age < 18:
                errors['date_of_birth'] = 'You must be at least 18 years old.'
        phone_number = attrs.get('phone_number')

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        CustomerModel.objects.update_or_create(
            user=user,
            defaults={
                'first_name': validated_data['first_name'],
                'last_name': validated_data['last_name'],
                'date_of_birth': validated_data['date_of_birth'],
                'phone_number': validated_data['phone_number']
            })
        return validated_data
