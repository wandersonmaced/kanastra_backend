# myapp/views.py
from rest_framework.generics import ListAPIView
from file_handling.model.file_models import Debt, DebtSerializer
from rest_framework.pagination import PageNumberPagination


# Define a custom paginator
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Default to 10 items per page
    page_size_query_param = 'page_size'  # Allow client to override, e.g., ?page_size=20
    max_page_size = 100  # Maximum limit allowed


# View
class DebtListView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    pagination_class = StandardResultsSetPagination
