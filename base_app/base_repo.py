from typing import Iterable
from django.db.models import Model, Q, QuerySet
from rest_framework.exceptions import NotFound


class BaseRepo:
    def __init__(self) -> None:
        self.model = Model
        self.model_objects = QuerySet
        self.filtered_objects = self.model_objects
        self.filter_fields = Iterable

    def resolve_lookup_fields(self, keyword, *fields):
        """Takes a tuple of lookup fields and returns a query expression"""
        Qr = None
        for field in fields:
            q = Q(**{f"{field}__icontains": keyword })
            if Qr:
                Qr = Qr | q # or & for filtering
            else:
                Qr = q
        return Qr


    def get_by_keyword(self, query_logic: dict):
        try:
            query_result = self.model_objects.get(**query_logic)
        except self.model.DoesNotExist:
            raise NotFound()
        return query_result

    def filter_by_dict(self, filter_dict: dict):
        self.filtered_objects = self.filtered_objects.filter(**filter_dict)
        return self.filtered_objects

    def filter_by_keyword(self, keyword: str):
        query_logic = self.resolve_lookup_fields(keyword, *self.filter_fields)
        self.filtered_objects = self.filtered_objects.filter(query_logic)
        return self.filtered_objects
    
    def filter_by_dict_or_keyword(self, filter_dict: dict, keyword: str):
        self.filtered_objects = self.all()
        if keyword:
            self.filtered_objects = self.filter_by_keyword(keyword)
        if filter_dict:
            self.filtered_objects = self.filter_by_dict(filter_dict)
        return self.filtered_objects

    def latest(self, field: str):
        query_result = self.model_objects.latest(field)
        return query_result

    def all(self):
        self.filtered_objects = self.model_objects.all()
        return self.filtered_objects

    def create(self, **kwargs):
        query_result = self.model_objects.create(**kwargs)
        return query_result    
        
    def bulk_create(self, *args):
        query_result = self.model_objects.bulk_create(
                list(map(lambda i: self.model(**i), args)), 
                ignore_conflicts=False
            )
        return query_result
        