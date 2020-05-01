from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 30
    max_page_size = 1000
    page_query_param = 'page'
    page_size_query_param = 'page_size'
