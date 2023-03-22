from rest_framework import serializers
from Inbox.models import Customer
from django.core.validators import RegexValidator



class CustomerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['status']

# Customer List
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ['message','files']

class EmailSerializer(serializers.ModelSerializer):
    cc = serializers.CharField()
    class Meta:
        model = Customer
        fields = ['id','name','email','cc','subject','message','files']

class MessageSerializer(serializers.ModelSerializer):
    # Name
    name = serializers.CharField(
        min_length=3, 
        max_length=50, 
        label='Name',
        required=True,
        validators=[RegexValidator(
            regex=r'^[A-Za-z ]+$',
            message="Name can only contain letters."
            )], 
        error_messages={'blank': 'Please enter your name.'},      
    )

    # Phone number
    phone = serializers.CharField(
        min_length=10, 
        max_length=12, 
        required=True,
        error_messages={'blank': 'Please enter your phone number.', 
                        'min_length': 'Phone field is incomplete'},
    )

    # Email
    email = serializers.EmailField(
        label='Email address',
        min_length=3, 
        max_length=50, 
        required=True,
        error_messages={'blank': 'Email cannot be empty !'},
    )

    # File (Upload resume)
    files = serializers.FileField(
        label='Choose File',
        error_messages={'invalid':'Please select a file to upload.'},
        required=False,
    )

    class Meta:
        model = Customer
        fields = [
            'name',
            'phone',
            'email',
            'subject',
            'message',
            'files',
        ]

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    # 1) CONVERSION
    def create(self, validated_data):
        validated_data['name'] = validated_data['name'].title() 

    # 2) RESTRICTION (file extensions- if statement + upload size control)
    def validate_files(self, value):
        # Variable
        EXT = ['rar', 'zip']
        ext = str(value).split('.')[-1]
        type = ext.lower()
        # Statement
        # a) Accept only rar - zip
        if type not in EXT:
            raise serializers.ValidationError('Only: rar or zip')
        # b) Prevent upload more than 5mb
        if value.size > 5 * 1048476:
            raise serializers.ValidationError('Denied ! Maximum allowed is 5mb.')
        return value
