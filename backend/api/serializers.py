from rest_framework import serializers
from .models import Advance, Transaction, User

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'src_bank_account', 'dst_bank_account', 'amount', 'direction', 'status']

class FiveDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'status', 'timestamp']

class AdvanceSerializer(serializers.ModelSerializer):
    src_bank_account = serializers.ReadOnlyField(source='src_bank_account.id')        
    class Meta:
        model = Advance
        fields = ['id', 'src_bank_account', 'dst_bank_account', 'amount']

