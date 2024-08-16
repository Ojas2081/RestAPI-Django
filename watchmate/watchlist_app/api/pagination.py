from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'p'
    page_size_query_param = 'size'


class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'
    max_limit = 10


class WatchListCPPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
