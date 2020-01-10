from rest_framework.filters import SearchFilter


class SearchVectorFilter(SearchFilter):
    search_vector_field_name = 'search_vector'

    def construct_search(self, field_name):
        if field_name == self.search_vector_field_name:
            return field_name
        return super().construct_search(field_name)
