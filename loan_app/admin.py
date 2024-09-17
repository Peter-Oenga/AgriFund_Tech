from django.contrib import admin
from . models import Borrower, LoanApplication, Loan

# Register your models here.

admin.site.register(Borrower)
admin.site.register(LoanApplication)
admin.site.register(Loan)