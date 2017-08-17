from jinja2 import Environment
from datetime import datetime
from api.services import multiple_replace


def _limit_text(value, num, dot=False):
    if len(value) > num:
        if dot:
            return value[:num] + '…'
        else:
            return value[:num]
    return value[:num]


def _pdf_to_png(path, sizes='w_250,h_250'):
    """Ex: w_300,h_200"""
    try:
        replace_dict = {
            '.pdf': '.png',
            '/image/upload/': '/image/upload/{sizes},c_fill/'.format(
                sizes=sizes),
        }
        return multiple_replace(path, replace_dict)
    except:
        return '/assets/img/dummy.png'


def _img_to_thumbnail(path, sizes='w_250,h_250'):
    """Ex: w_300,h_200"""
    try:
        replace_dict = {
            '/image/upload/': '/image/upload/{sizes},'.format(sizes=sizes),
        }
        return multiple_replace(path, replace_dict)
    except:
        return path


def _filter_datetime(date, fmt='%Y-%m-%d %H:%M'):
    try:
        try:
            date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f')
        except:
            date = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            date = datetime.strptime(str(date), '%Y-%m-%d')
        except:
            return ''

    return date.strftime(fmt)


def environment(**options):
    env = Environment(**options)
    env.globals.update({
    })
    env.filters.update({
        'limit_text': _limit_text,
        'datetime': _filter_datetime,
        'pdf_to_png': _pdf_to_png,
        'img_to_thumbnail': _img_to_thumbnail,
    })
    return env
