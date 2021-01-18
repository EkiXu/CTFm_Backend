from collections import OrderedDict
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class ScoreboardPagination(LimitOffsetPagination):
    def get_paginated_response(self, data,challenge_list):
        return Response(OrderedDict([
            ('challenges',challenge_list),
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))