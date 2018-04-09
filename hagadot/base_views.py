import functools

from django.http import HttpResponse
from django.utils.decorators import method_decorator


def allow_cors(f):
    @functools.wraps(f)
    def df(*args, **kwargs):
        response = f(*args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response[
            "Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response

    return df


class AllowCORSMixin(object):
    @method_decorator(allow_cors)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        return HttpResponse()
