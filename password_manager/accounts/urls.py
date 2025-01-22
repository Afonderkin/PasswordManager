from django.urls import path
from .views import AccountsListCreateView, AccountsDetailView, DecryptPasswordView


urlpatterns = [
    path('', AccountsListCreateView.as_view(), name='accounts-list-create'),
    path('<int:pk>/', AccountsDetailView.as_view(), name='accounts-detail'),
    path('<int:pk>/decrypt-password/', DecryptPasswordView.as_view(), name='decrypt-password'),
]