# -*- coding: utf-8 -*-

from rest_api.errors import ResponseMissingFields, ResponseMustBeLoggedIn, ResponseNotAllowed


def get_data(keys, default={}, optional=False, method="POST"):
    def get_data_wrap(function):
        def get_data_decorator(self, request, **kwargs):
            tab = getattr(request, method, [])
            fields = []
            data = {}
            for key in keys:
                if key in tab:
                    data[key] = tab[key]
                elif key in default:
                    data[key] = default[key]
                elif isinstance(optional, bool) and not optional or isinstance(optional, list) and key not in optional:
                    fields.append(str(key))
            if len(fields):
                raise ResponseMissingFields(fields)
            return function(self, request=request, data=data, **kwargs)
        return get_data_decorator
    return get_data_wrap


def must_be_in_rights(rights):
    def must_be_in_rights_wrap(function):
        def must_be_in_rights_decorator(self, session, **kwargs):
            if not session or not session.is_connected():
                raise ResponseMustBeLoggedIn()
            if not session.check_right(rights):
                raise ResponseNotAllowed()
            return function(self, session=session, **kwargs)
        return must_be_in_rights_decorator
    return must_be_in_rights_wrap


def must_be_connected(function):
    def must_be_connected_decorator(self, session, **kwargs):
        if not session or not session.is_connected():
            raise ResponseMustBeLoggedIn()
        return function(self, session=session, **kwargs)
    return must_be_connected_decorator
