# -*- coding: utf-8 -*-


class ResponseError(Exception):
    def __init__(self, error, details=None, code=400):
        self.error = error
        self.details = details or []
        self.code = code

    def get_response(self):
        data = {'error': self.error, 'error_code': self.code, 'error_details': self.details}
        from rest_api.API import API
        return API.make_response(data, self.code)


class ResponseNotFound(ResponseError):
    def __init__(self, error="Not Found", details=None, code=404):
        super().__init__(error, details, code)


class ResponseForbidden(ResponseError):
    def __init__(self, error="Forbidden", details=None, code=403):
        super().__init__(error, details, code)


class ResponseNotImplemented(ResponseError):
    def __init__(self, error="Not Implemented", details=None, code=501):
        super().__init__(error, details, code)


class ResponseMethodNotAllowed(ResponseError):
    def __init__(self, error="Method Not Allowed", details=None, code=405):
        super().__init__(error, details, code)


class ResponseMissingFields(ResponseError):
    def __init__(self, fields=None):
        self.fields = fields
        super().__init__("You must provide all mandatory fields.", details=fields)


class ResponseMustBeLoggedIn(ResponseForbidden):
    def __init__(self):
        super().__init__("You must be logged in to access this action.")


class ResponseNotAllowed(ResponseForbidden):
    def __init__(self):
        super().__init__("You are not allowed to access to this action.")


class ResponseNotAllowedFilter(ResponseForbidden):
    def __init__(self):
        super().__init__("You are not allowed to filter this field.")


class ResponseNoFilter(ResponseError):
    def __init__(self):
        super().__init__("You must define at least one field.")


class ResponseBadOrder(ResponseError):
    def __init__(self):
        super().__init__("The value of sort must be 'asc' or 'desc'.")


class ResponsePaginationBadLimit(ResponseError):
    def __init__(self):
        super().__init__("Bad parameter 'limit'.")


class ResponsePaginationBadPage(ResponseError):
    def __init__(self):
        super().__init__("Bad parameter 'page'.")


class ResponsePaginationEmptyPage(ResponseError):
    def __init__(self):
        super().__init__("The parameter 'page' is too large (empty page).")
