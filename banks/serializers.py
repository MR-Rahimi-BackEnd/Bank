from rest_framework import serializers
from .models import Bank, StarUser, TransactionReceipt, Walet, Transaction, TransactionType


class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id','phone' ,'user', 'amount', 'bank_name']


class WaletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walet
        fields = ['id', 'phone', 'amount']


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')
    receiver = serializers.CharField(source='receiver.username', required=False)
    transaction_type = serializers.CharField(source='transaction_type.name')

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'transaction_type', 'created_at']


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['id', 'name']
class TransactionReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionReceipt
        fields = '__all__'
        
        
class StarUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StarUser
        fields = ['star']