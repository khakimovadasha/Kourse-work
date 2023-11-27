from rest_framework.pagination import PageNumberPagination

class PagesPagination(PageNumberPagination):  
    page_size = 5