from rest_framework.filters import SearchFilter


class SearchVectorFilter(SearchFilter):
    """
    Sub-classing `SearchFilter` to force the full-text search capabilities of postgres when a search vector is defined.
    For example, if there is a SearchVectorField defined as "search_vector" then you can directly filter like the following:
        Recipe.objects.filter(search_vector='cheeses')
    """
    search_vector_field_name = 'search_vector'

    def construct_search(self, field_name):
        if field_name == self.search_vector_field_name:
            return field_name
        return super().construct_search(field_name)
