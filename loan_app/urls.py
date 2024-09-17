# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BorrowerViewSet, LoanApplicationViewSet, LoanViewSet

router = DefaultRouter()
router.register(r'borrowers', BorrowerViewSet)
router.register(r'loanapplications', LoanApplicationViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
