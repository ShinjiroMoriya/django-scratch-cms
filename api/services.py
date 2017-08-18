import re
import ast
import time
import functools
from math import ceil, floor
from datetime import timedelta
from jinja2 import Markup
from django.contrib.messages import get_messages
from django.conf import settings
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def calc_time(message='', parser=None):
    """
    :計測用のデコレーター
    """
    def _calc_time(func):
        @functools.wraps(func)
        def wrapper(*args, **kargs):
                request = args[1]
                start = time.time()
                ret = func(*args, **kargs)
                if settings.DEBUG:
                    if parser:
                        parsed_message = parser(message, *args, **kargs)
                        print(request.path +
                              " end time : {time} sec : "
                              "{parsed_message}".format(
                                  time=(time.time() - start),
                                  parsed_message=parsed_message))
                    else:
                        print(request.path +
                              " end time : {time} sec : {message}".format(
                                time=(time.time() - start),
                                message=message))
                return ret
        return wrapper
    return _calc_time


def time_seconds(days=7):
    """
    :秒を返す
    """
    return timedelta(days=days).total_seconds()


def get_error_message(request: object) -> dict or None:
    """
    :Get Flash Error Message
    """
    error_message = None
    if get_messages(request):
        message_storage = get_messages(request)
        for message in message_storage:
            error_message = str(message)
        error_message = ast.literal_eval(error_message)
    return error_message


def session_delete(request, data: list):
    """
    :セッション削除用
    """
    for i in data:
        try:
            del request.session[i]
        except KeyError:
            pass


class Pagination:
    """
    :ページャー
    """
    def __init__(self, page: int, per_page: int, total: int, slug: str,
                 query_order=''):
        self.page = int(page)
        self.slug = slug
        self.per_page = per_page
        self.total = total
        self.pages = int(ceil(self.total / float(self.per_page)))
        self.offset = (int(page) - 1) * int(per_page)
        self.query_order = query_order

    def numbers(self, number: int=5, current: int=1):
        total_page = ceil(self.total / self.per_page)
        if total_page < number:
            number = total_page

        number_harf = floor(number / 2)
        number_start = int(current) - number_harf
        number_end = int(current) + number_harf

        if number_start <= 0:
            number_start = 1
            number_end = number

        if number_end > total_page:
            number_start = total_page - number + 1
            number_end = total_page

        return {'start': number_start, 'end': number_end + 1}

    def prev(self):
        if self.page > 1:
            return self.slug + str(self.page - 1)

    def next(self):
        if self.page < self.pages:
            return self.slug + str(self.page + 1)


def page_information(current, total, per_page):
    """
    :ページ表示情報
    """
    current = int(current)
    total = int(total)
    per_page = int(per_page)

    start = current if current == 1 else current-1
    end = ceil(total / per_page)
    number_total = total
    number_start = 1 if current == 1 else (start * per_page) + 1

    if total == 0:
        return '0件を表示'

    number_end = total if current == end else (current * per_page)

    return (str(number_total) + '件中' + str(number_start) +
            '-' + str(number_end) + '件を表示')


def no_bleak(value):
    """
    :改行を消す
    """
    return value.replace('\n', '')


def nl2br(value):
    """
    :改行コードを<br>に変換
    """
    return Markup(value.replace('\n', '<br>'))


def string_to_date(date: str, fmt='%Y-%m-%d'):
    """
    :文字列をDate形式に変換
    :%Y-%m-%d %H:%M:%S
    """
    try:
        return datetime.strptime(date, fmt)
    except:
        return None


def date_format(date, fmt='%Y-%m-%d %H:%M') -> str:
    """
    :日付の型を変更
    """
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


def get_image_url_content(contents):
    img_url = []
    pattern_img_tag = re.compile('<img[\s]*src[\s]*=.*?>')
    pattern_img_src = re.compile('src[\s]*="(.*?)"')
    img_tag = pattern_img_tag.findall(contents)
    for i in img_tag:
        try:
            m = pattern_img_src.search(i)
            img_url.append(m.group(1))
        except:
            pass
    return img_url


def get_pdf_url_content(contents):
    pdf_url = []
    pattern_pdf_tag = re.compile('<a[\s]*href[\s]*=.*?>')
    pattern_pdf_src = re.compile('href[\s]*="(.*?.pdf)"')
    pdf_tag = pattern_pdf_tag.findall(contents)
    for i in pdf_tag:
        try:
            m = pattern_pdf_src.search(i)
            pdf_url.append(m.group(1))
        except:
            pass
    return pdf_url


def get_url_content(contents):
    url = []
    pattern_url = re.compile('(https?://[\w/:%#$&?()~.=+\-]+)')
    urls = pattern_url.findall(contents)
    for i in urls:
        try:
            m = pattern_url.search(i)
            url.append(m.group(1))
        except:
            pass
    return list(set(urls))


def get_url_title(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '59.0.3071.115 Safari/537.36'
        }
        req = Request(url, headers=headers)
        html = urlopen(req)
        soup = BeautifulSoup(html, 'html.parser')
        return soup.title.string

    except:
        return None


def multiple_replace(text, adict):
    """
    一度に複数の文字列を置換する.
    - text中からディクショナリのキーに合致する文字列を探し、対応の値で置換して返す
    """
    # マッチさせたいキー群を正規表現の形にする e.g) (a1|a2|a3...)
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]

    return rx.sub(one_xlat, text)