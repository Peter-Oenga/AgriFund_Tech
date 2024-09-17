# serializers.py
from rest_framework import serializers
from .models import Borrower, LoanApplication, Loan

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id', 'user', 'phone', 'id_number']

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = ['id', 'borrower', 'principal', 'loan_term_days', 'processing_fee', 'interest_rate', 'status', 'applied_at']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'loan_application', 'borrower', 'principal', 'total_amount', 'loan_term_days', 'disbursement_amount', 'interest_rate', 'repaid_amount', 'is_fully_repaid', 'applied_at', 'disbursed_at', 'due_date']
