from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import LoanApplication, Loan, Borrower


# views.py
from rest_framework import viewsets
from .models import Borrower, LoanApplication, Loan
from .serializers import BorrowerSerializer, LoanApplicationSerializer, LoanSerializer

class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer

class LoanApplicationViewSet(viewsets.ModelViewSet):
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


# List all loan applications (admin view)
class LoanApplicationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LoanApplication
    template_name = 'loan_application_list.html'  # Add template path
    context_object_name = 'applications'

    def test_func(self):
        # Only staff or admin can view loan applications
        return self.request.user.is_staff or self.request.user.is_superuser

# Create a loan application (user view)
class LoanApplicationCreateView(LoginRequiredMixin, CreateView):
    model = LoanApplication
    # Add your form here
    template_name = 'loan_application_form.html'  # Add template path
    success_url = reverse_lazy('loan_application_list')  # Redirect after submission

    def form_valid(self, form):
        form.instance.borrower = self.request.user  # Set borrower to current user
        return super().form_valid(form)

# Update a loan application (staff/admin)
class LoanApplicationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LoanApplication
    fields = ['status']  # Only allow admin to update the status
    template_name = 'loan_application_form.html'
    success_url = reverse_lazy('loan_application_list')

    def test_func(self):
        # Only staff or admin can update loan applications
        return self.request.user.is_staff or self.request.user.is_superuser

# Delete a loan application (admin view)
class LoanApplicationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LoanApplication
    template_name = 'loan_application_confirm_delete.html'
    success_url = reverse_lazy('loan_application_list')

    def test_func(self):
        # Only staff or admin can delete loan applications
        return self.request.user.is_staff or self.request.user.is_superuser




# List all loans (for borrowers to see their loans and staff to manage them)
class LoanListView(LoginRequiredMixin, ListView):
    model = Loan
    template_name = 'loan_list.html'  # Add template path
    context_object_name = 'loans'

    def get_queryset(self):
        # Borrowers can only see their own loans, staff sees all
        if self.request.user.is_staff:
            return Loan.objects.all()
        else:
            return Loan.objects.filter(borrower=self.request.user)

# Create a loan (admin creates it after loan application approval)
class LoanCreateView(LoginRequiredMixin, CreateView):
    model = Loan
     # Form for loan creation (interest rate, terms, etc.)
    template_name = 'loan_form.html'  # Add template path
    success_url = reverse_lazy('loan_list')

    def form_valid(self, form):
        form.instance.borrower = self.request.user  # Set borrower to current user
        return super().form_valid(form)

# Update a loan (admin functionality)
class LoanUpdateView(LoginRequiredMixin, UpdateView):
    model = Loan
    # Reuse the loan form for updating
    template_name = 'loan_form.html'
    success_url = reverse_lazy('loan_list')

# Delete a loan (admin functionality)
class LoanDeleteView(LoginRequiredMixin, DeleteView):
    model = Loan
    template_name = 'loan_confirm_delete.html'
    success_url = reverse_lazy('loan_list')




# List all borrowers (admin view)
class BorrowerListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Borrower
    template_name = 'borrower_list.html'  # Path to your borrower listing template
    context_object_name = 'borrowers'

    def test_func(self):
        # Only staff or admin can view borrowers
        return self.request.user.is_staff or self.request.user.is_superuser

# Create a borrower (admin functionality)
class BorrowerCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Borrower
    # Form for creating borrowers
    template_name = 'borrower_form.html'  # Path to borrower creation template
    success_url = reverse_lazy('borrower_list')

    def form_valid(self, form):
        # Ensure the user associated with the borrower is a valid user
        user = get_object_or_404(User, id=self.request.POST.get('user'))
        form.instance.user = user
        return super().form_valid(form)

    def test_func(self):
        # Only staff or admin can create borrowers
        return self.request.user.is_staff or self.request.user.is_superuser

# Update a borrower (admin functionality)
class BorrowerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Borrower
    template_name = 'borrower_form.html'
    success_url = reverse_lazy('borrower_list')

    def test_func(self):
        # Only staff or admin can update borrowers
        return self.request.user.is_staff or self.request.user.is_superuser

# Delete a borrower (admin functionality)
class BorrowerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Borrower
    template_name = 'borrower_confirm_delete.html'
    success_url = reverse_lazy('borrower_list')

    def test_func(self):
        # Only staff or admin can delete borrowers
        return self.request.user.is_staff or self.request.user.is_superuser



