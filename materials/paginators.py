from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    """Кастомный пагинатор для курсов и уроков"""

    page_size = 5  # Количество элементов на одной странице по умолчанию
    page_size_query_param = (
        "page_size"  # Позволяет клиенту менять размер страницы через URL (?page_size=10)
    )
    max_page_size = 50  # Максимально разрешенный размер страницы
