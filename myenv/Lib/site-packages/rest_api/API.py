# -*- coding: utf-8 -*-

import json
from django.conf import settings
from django.conf.urls import patterns, url
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils.module_loading import import_string
from rest_api.errors import *


class API(object):
    api_name = ""
    format_object = {}

    def __init__(self):
        class_name = self.__class__.__name__
        name_bits = [bit for bit in class_name.split('API') if bit]
        resource_name = ''.join(name_bits).lower()
        self.resource_name = resource_name
        self.cookies = []
        self.is_list = False

    """
        Responses
    """
    @staticmethod
    def make_response(data=None, code=200):
        if data is not None:
            data = json.dumps(data, cls=DjangoJSONEncoder)
        return HttpResponse(content=data, status=code, content_type="application/json")

    def response(self, data=None, code=200):
        response = self.make_response(data, code)
        for cookie in self.cookies:
            response.set_cookie(*cookie['args'], **cookie['kwargs'])
        return response

    """
        URLS
    """
    def prepend_urls(self):
        return []

    @property
    def urls(self):
        urls = self.prepend_urls()
        urls.append(url(r"^%s(/?)$" % self.resource_name, self.dispatch_api("list")))
        urls.append(url(r"^%s/(?P<_id>[0-9]+)(/?)$" % self.resource_name, self.dispatch_api("detail")))
        return patterns('', *urls)

    """
        Cookies
    """
    def add_cookie(self, *args, **kwargs):
        self.cookies.append({"args": args, "kwargs": kwargs})

    """
        Format results
    """
    def format(self, obj, _format=None):
        _format = self.format_object if not _format else _format
        data = dict()
        for field in _format:
            if not self.is_list or _format[field].get("list", True):
                if "object" in _format[field]:
                    if "object_list" in _format[field]:
                        data[field] = list()
                        sub_obj = getattr(obj, _format[field].get("object_list", {})).all()
                        if "object_list_order" in _format[field]:
                            sub_obj = sub_obj.order_by(_format[field].get("object_list_order", {}))
                        for sub_item in sub_obj:
                            data[field].append(self.format(sub_item, _format[field].get("object", {})))
                    else:
                        data[field] = self.format(obj, _format[field].get("object", {}))
                else:
                    data[field] = self._get_attribute(obj, _format[field].get("field", field))
        return data

    def _get_attribute(self, instance, name):
        if hasattr(instance, name):
            return getattr(instance, name)
        names = name.split('__')
        name = names.pop(0)
        if len(names) == 0:
            return None
        if hasattr(instance, name):
            value = getattr(instance, name)
            if value is None:
                return None
            return self._get_attribute(value, "__".join(names))
        return None

    def _get_format_keys(self, _format=None):
        _format = self.format_object if not _format else _format
        data = dict()
        for field in _format:
            if not self.is_list or _format[field].get("list", True):
                if "object" in _format[field]:
                    data[field] = self._get_format_keys(_format[field].get("object", {}))
                else:
                    data[field] = _format[field].get("field", field)
        return data

    def _get_authorized_keys(self, _format=None):
        _format = self.format_object if not _format else _format
        data = []
        for field in _format:
            if not self.is_list or _format[field].get("list", True):
                if "object" in _format[field]:
                    data += self._get_authorized_keys(_format[field].get("object", {}))
                else:
                    data.append(_format[field].get("field", field))
        return data

    """
        Filters results
    """
    def _apply_filter_data(self, request, data, authorized_keys=None):
        if "filter" not in request.GET:
            return data
        authorized_keys = self._get_authorized_keys() if not authorized_keys else authorized_keys
        field_filter = request.GET["filter"]
        if field_filter not in authorized_keys:
            raise ResponseNotAllowedFilter()
        filters = dict()
        filters_available = ["exact", "iexact", "contains", "icontains", "gt", "gte", "lt", "lte", "startswith",
                             "istartswith", "endswith", "iendswith", "isnull", "regex", "iregex"]
        for elem in filters_available:
            if elem in request.GET:
                filters[field_filter + "__" + elem] = request.GET[elem]
        if not len(filters):
            raise ResponseNoFilter()
        return data.filter(**filters)

    """
        Sort results
    """
    def _apply_order_data(self, request, data, authorized_keys=None):
        if "order" not in request.GET:
            return data
        authorized_keys = self._get_authorized_keys() if not authorized_keys else authorized_keys
        order = request.GET["order"]
        if order not in authorized_keys:
            raise ResponseNotAllowedFilter()
        sort = request.GET.get("sort", "asc")
        if sort not in ["asc", "desc"]:
            raise ResponseBadOrder()
        return data.order_by(order if sort == "asc" else "-" + order)

    """
        API pagination
    """
    def pagination(self, request, data, _filter=True, _order=True):
        self.is_list = True
        authorized_keys = self._get_authorized_keys()
        if _filter:
            data = self._apply_filter_data(request, data, authorized_keys)
        if _order:
            data = self._apply_order_data(request, data, authorized_keys)
        try:
            limit = int(request.GET.get('limit', 25))
            limit = 1 if limit < 1 else limit
            limit = 100 if limit > 100 else limit
        except (TypeError, ValueError):
            raise ResponsePaginationBadLimit()
        try:
            current_page = int(request.GET.get('page', 1))
            current_page = 1 if current_page < 1 else current_page
        except (TypeError, ValueError):
            raise ResponsePaginationBadPage()
        paginator = Paginator(data, limit)
        try:
            page = paginator.page(current_page)
        except PageNotAnInteger:
            raise ResponsePaginationBadPage()
        except EmptyPage:
            raise ResponsePaginationEmptyPage()
        return {
            "current_page": current_page,
            "limit": limit,
            "number_pages": paginator.num_pages,
            "total_results": paginator.count,
            "count_results": len(page),
            "format": self._get_format_keys(),
            "results": page
        }

    """
        Dispatch route API
    """
    def dispatch_api(self, view="list"):
        def wrapper(request, *args, **kwargs):
            try:
                self.is_list = False
                if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META:
                    request.method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE']
                method = request.method.lower()
                if method == "head":
                    method = "get"
                if method not in ["get", "post", "put", "patch", "delete"]:
                    raise ResponseMethodNotAllowed()
                function = getattr(self, "method_%s_%s" % (method, view), None)
                if function is None:
                    raise ResponseMethodNotAllowed()
                if method != "get":
                    request.method = "POST"
                if 'CONTENT_TYPE' in request.META and request.META['CONTENT_TYPE'].startswith('application/json'):
                    try:
                        request.POST = json.loads(request.body.decode('utf-8'))
                    except:
                        pass
                if not hasattr(settings, "REST_AUTH_SESSION_ENGINE"):
                    session = None
                    # from django.core.exceptions import ImproperlyConfigured
                    # raise ImproperlyConfigured("You must defined 'REST_AUTH_SESSION_ENGINE' in settings")
                else:
                    session = import_string(settings.REST_AUTH_SESSION_ENGINE)(request)
                if "_id" in kwargs:
                    kwargs["_id"] = int(kwargs["_id"])
                if "_id2" in kwargs:
                    kwargs["_id2"] = int(kwargs["_id2"])
                response = function(session=session, request=request, **kwargs)
                if not isinstance(response, HttpResponse):
                    return self.response(data=None, code=204)
            except ResponseError as e:
                return e.get_response()
            except Exception as e:
                if not settings.DEBUG:
                    return self.response({'error': str(e), 'error_code': 500, 'error_details': None}, 500)
                raise
            return response
        return wrapper
