from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Extending the default user with additional fields for borrowers
class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    id_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.username} - Borrower"


class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    loan_term_days = models.IntegerField()
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application {self.id} - {self.borrower.username} - {self.status}"




class Loan(models.Model):
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    principal = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_term_days = models.IntegerField()
    disbursement_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    repaid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_fully_repaid = models.BooleanField(default=False)
    applied_at = models.DateTimeField()
    disbursed_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()

    def calculate_total_amount(self):
        interest_amount = (self.principal * self.interest_rate) / 100
        self.total_amount = self.principal + interest_amount + self.processing_fee
        return self.total_amount

    def __str__(self):
        return f"Loan {self.id} - {self.borrower.username}"

