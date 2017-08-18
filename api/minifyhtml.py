from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.html import strip_spaces_between_tags as minify_html


class MinifyHTMLMiddleware(object):
    def __init__(self, get_response):
        if settings.DEBUG:
            raise MiddlewareNotUsed()
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    @staticmethod
    def process_response(_, response):
        if 'text/html' in response['Content-Type']:
            try:
                response.content = minify_html(response.content.strip())
            except DjangoUnicodeDecodeError:
                pass
        return response
