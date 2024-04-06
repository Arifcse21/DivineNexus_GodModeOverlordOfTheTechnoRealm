from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    # page_size = 10  # Set the number of items per page
    page_size_query_param = 'page_size'  # Allow clients to override the page size
    # max_page_size = 1000  # Set a maximum page size to prevent abuse
    def get_page_size(self, request):
        if self.page_size_query_param in request.query_params:
            return int(request.query_params[self.page_size_query_param])
        return self.page_size or 3
    
    def get_paginated_response(self, data):
        start_item = (self.page.number - 1) * self.get_page_size(self.request) + 1
        end_item = start_item + len(data) - 1
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data,
            'start_item': start_item,
            'end_item': end_item,
        })
# GET /your-api-endpoint/?page_size=20
# GET /your-api-endpoint/?page=1
# GET /your-api-endpoint/?page=2
