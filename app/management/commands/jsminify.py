from slimit import minify
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        def minify_js(src):
            return minify(src, mangle=True, mangle_toplevel=True)

        def do_jsmin(js_sources):
            for source in js_sources:
                with open(source + '.js') as file:
                    src = file.read()
                    min_data = minify_js(src)
                    f = open(dist.get(source) + '.min.js', 'w')
                    f.write(min_data)
                    f.close()

        sources = [
            'resources/js/script',
        ]

        dist = {
            'resources/js/script': 'assets/js/script',
        }

        do_jsmin(sources)
