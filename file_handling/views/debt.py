from rest_framework.generics import ListAPIView
from file_handling.model.file_models import Debt, DebtSerializer
from rest_framework.pagination import PageNumberPagination


#
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



class DebtListView(ListAPIView):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer
    pagination_class = StandardResultsSetPagination
