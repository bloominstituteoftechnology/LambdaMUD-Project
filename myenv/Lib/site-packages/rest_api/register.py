# -*- coding: utf-8 -*-

from rest_api.errors import ResponseNotFound
from django.conf.urls import patterns, url, include


class RegisterAPI(object):
    def __init__(self, api_name=""):
        self.api_name = api_name
        self._registry = {}

    def register(self, api):
        self._registry[api.resource_name] = api

    def unregister(self, resource_name):
        if resource_name in self._registry:
            del (self._registry[resource_name])

    @staticmethod
    def prepend_urls():
        return []

    @staticmethod
    def error_api():
        def wrapper(*args, **kwargs):
            return ResponseNotFound().get_response()
        return wrapper

    @property
    def urls(self):
        patterns_list = []
        for name in sorted(self._registry.keys()):
            self._registry[name].api_name = self.api_name
            patterns_list.append(url(r"^%s(/?)" % self.api_name, include(self._registry[name].urls)))
        patterns_list.append(url(r"^", self.error_api()))
        urls = self.prepend_urls()
        urls += patterns('', *patterns_list)
        return urls
