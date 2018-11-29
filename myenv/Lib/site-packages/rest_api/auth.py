# -*- coding: utf-8 -*-


class BaseAuthREST(object):
    def is_connected(self):
        raise Exception("Not implemented")

    def check_right(self, rights, _all=False):
        raise Exception("Not implemented")

