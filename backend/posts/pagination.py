from rest_framework.pagination import CursorPagination, PageNumberPagination


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class FeedPagination(CursorPagination):
    page_size = 15
    ordering = '-created_at'
