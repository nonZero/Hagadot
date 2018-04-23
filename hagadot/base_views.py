import functools

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View


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


class SimpleJsonView(AllowCORSMixin, View):
    def get(self, request):
        data = self.get_data()
        return JsonResponse(data, safe=False)
