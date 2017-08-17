import sys
from datetime import datetime
from rest_framework import viewsets, pagination
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View
from django.db import transaction
from django.http import Http404
from django.contrib.auth import logout, authenticate, login
from app.serializer import *
from app.forms import *
from api.cloudinary import set_image_upload, set_pdf_upload, delete_resources
from api.logger import logger
from api.services import (get_error_message, Pagination, page_information,
                          date_format, string_to_date, session_delete,
                          get_image_url_content, get_pdf_url_content)


class PostResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10


class PostAPIView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'post_id'
    lookup_value_regex = '[\w\-]+'
    queryset = Post.get_published()
    serializer_class = PostSerializer
    pagination_class = PostResultsSetPagination


class PostImageAPIView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'image_id'
    lookup_value_regex = '[\w\-]+'
    queryset = PostImage.get_all()
    serializer_class = PostImageSerializer
    filter_fields = ('image_id',)


class PostPdfAPIView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'pdf_id'
    lookup_value_regex = '[\w\-]+'
    queryset = PostPdf.get_all()
    serializer_class = PostPdfSerializer
    filter_fields = ('pdf_id',)


class PostSetup(View):
    def __init__(self, **kwargs):
        self.request_data = {}
        self.error_messages = {}
        self.form_data = {}
        self.data = {}
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':

            self.request_data = request.session.get('request_data')
            self.error_messages = request.session.get('error_messages')
            self.form_data = request.session.get('form_data')

            session_delete(request, [
                'request_data', 'error_messages', 'form_data'])

            self.data.update({
                'request_data': self.request_data,
                'form_data': self.form_data,
                'messages': self.error_messages,
            })
        return super().dispatch(request, *args, **kwargs)


class PostImageIndex(PostSetup):
    def get(self, request, page=1):
        total = PostImage.get_all().count()

        paginate = Pagination(page=page, per_page=10, total=total,
                              slug='/post/image/page/')

        pageinformation = page_information(current=page,
                                           total=total, per_page=10)

        post_images = PostImage.get_all()[
                      paginate.offset:
                      paginate.offset + paginate.per_page]

        self.data.update({
            'title': '画像一覧',
            'post_images': post_images,
            'pageinformation': pageinformation,
            'pagination': paginate,
        })
        return render(request, 'post_image.html', {'data': self.data})


class PostImageAdd(View):
    @staticmethod
    def post(request):
        file = request.FILES.get('image_file')
        if file is None:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)

        status, image_data = set_image_upload(file)

        if status == 500:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)
        try:
            PostImage.create_image({
                'title': image_data.get('title'),
                'image_id': image_data.get('image_id'),
                'image_url': image_data.get('image_url'),
            })

            return JsonResponse({
                'status': 200,
                'image_id': image_data.get('image_id'),
                'image_url': image_data.get('image_url'),
                'message': 'Success'
            }, status=200)

        except:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)


class PostImageDelete(View):
    @staticmethod
    def get(request, image_id):
        post_image = PostImage.get_by_image_id(image_id)
        use_count = post_image.post_image.all().count()

        if post_image is None and use_count != 0:
            request.session['request_data'] = {
                'delete_status': 'Error',
            }
            return redirect(request.META.get('HTTP_REFERER', '/'))

        sid = transaction.savepoint()
        try:
            delete_resources([image_id])
            PostImage.delete_image(image_id)
            transaction.savepoint_commit(sid)

        except:
            request.session['request_data'] = {
                'delete_status': 'Error',
            }
            transaction.savepoint_rollback(sid)

        return redirect(request.META.get('HTTP_REFERER', '/'))


class PostPdfIndex(PostSetup):
    def get(self, request, page=1):
        total = PostPdf.get_all().count()

        paginate = Pagination(page=page, per_page=10, total=total,
                              slug='/post/pdf/page/')

        pageinformation = page_information(current=page,
                                           total=total, per_page=10)

        post_pdfs = PostPdf.get_all()[
                      paginate.offset:
                      paginate.offset + paginate.per_page]

        self.data.update({
            'title': 'PDF一覧',
            'post_pdfs': post_pdfs,
            'pageinformation': pageinformation,
            'pagination': paginate,
        })
        return render(request, 'post_pdf.html', {'data': self.data})


class PostPdfAdd(View):
    @staticmethod
    def post(request):
        file = request.FILES.get('pdf_file')
        if file is None:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)

        status, pdf_data = set_pdf_upload(file)

        if status == 500:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)
        try:
            PostPdf.create_pdf({
                'title': pdf_data.get('title'),
                'pdf_id': pdf_data.get('pdf_id'),
                'pdf_url': pdf_data.get('pdf_url'),
            })

            return JsonResponse({
                'status': 200,
                'title': pdf_data.get('title'),
                'pdf_id': pdf_data.get('pdf_id'),
                'pdf_url': pdf_data.get('pdf_url'),
                'message': 'Success'
            }, status=200)

        except:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)


class PostPdfDelete(View):
    @staticmethod
    def get(request, pdf_id):
        post_pdf = PostPdf.get_by_pdf_id(pdf_id)
        use_count = post_pdf.post_pdf.all().count()

        if post_pdf is None and use_count != 0:
            request.session['request_data'] = {
                'delete_status': 'Error',
            }
            return redirect(request.META.get('HTTP_REFERER', '/'))

        sid = transaction.savepoint()
        try:
            delete_resources([pdf_id])
            PostPdf.delete_pdf(pdf_id)
            transaction.savepoint_commit(sid)

        except:
            request.session['request_data'] = {
                'delete_status': 'Error',
            }
            transaction.savepoint_rollback(sid)

        return redirect(request.META.get('HTTP_REFERER', '/'))


class PostIndex(View):
    @staticmethod
    def get(request, page=1):
        total = Post.get_all().count()

        paginate = Pagination(page=page, per_page=10, total=total,
                              slug='/post/page/')

        pageinformation = page_information(current=page,
                                           total=total, per_page=10)

        post = Post.get_all()[
                   paginate.offset:
                   paginate.offset + paginate.per_page]

        data = {
            'title': 'ニュース一覧',
            'post': post,
            'pageinformation': pageinformation,
            'pagination': paginate,
        }
        return render(request, 'post.html', {'data': data})


class PostCreate(PostSetup):
    def get(self, request):
        date_now = str(date_format(datetime.now(), fmt='%Y-%m-%d %H:%M'))
        self.data.update({
            'title': '新規追加',
            'date_now': date_now,
        })
        return render(request, 'post_create.html', {'data': self.data})

    @staticmethod
    def post(request):
        form = PostForm(request.POST)
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))
        if form.is_valid():
            registration_date = string_to_date(
                form.cleaned_data.get('publish_date'),
                fmt='%Y-%m-%d %H:%M')
            if registration_date is None:
                request.session['request_data'] = {
                    'post_status': 'Error',
                }
                request.session['form_data'] = form.cleaned_data
                return redirect(request.META.get('HTTP_REFERER', '/'))

            sid = transaction.savepoint()
            try:
                post = Post.create_post(form.cleaned_data)
                img_url = get_image_url_content(
                    form.cleaned_data.get('contents'))
                PostImage.add_use_post(img_url, post.post_id)
                pdf_url = get_pdf_url_content(
                    form.cleaned_data.get('contents'))
                PostPdf.add_use_post(pdf_url, post.post_id)
                transaction.savepoint_commit(sid)

            except:
                transaction.savepoint_rollback(sid)
                request.session['request_data'] = {
                    'post_status': 'Error',
                }
                request.session['form_data'] = form.cleaned_data
                return redirect(request.META.get('HTTP_REFERER', '/'))

        else:
            request.session['request_data'] = {
                'post_status': 'Error',
            }
            request.session['form_data'] = form.cleaned_data
            request.session['error_messages'] = get_error_message(request)

            return redirect(request.META.get('HTTP_REFERER', '/'))

        return redirect('/post')


class PostEdit(PostSetup):
    def get(self, request, post_id):
        post = Post.get_by_id(post_id)
        if post is None:
            raise Http404

        date_now = str(date_format(datetime.now(), fmt='%Y-%m-%d %H:%M'))
        self.data.update({
            'title': '編集',
            'date_now': date_now,
            'post': post,
        })
        return render(request, 'post_edit.html', {'data': self.data})

    @staticmethod
    def post(request, post_id):
        post = Post.get_by_id(post_id)
        if post is None:
            raise Http404

        form = PostForm(request.POST)
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))
        if form.is_valid():
            registration_date = string_to_date(
                form.cleaned_data.get('publish_date'),
                fmt='%Y-%m-%d %H:%M')
            if registration_date is None:
                request.session['request_data'] = {
                    'post_status': 'Error',
                }
                request.session['form_data'] = form.cleaned_data
                return redirect(request.META.get('HTTP_REFERER', '/'))

            sid = transaction.savepoint()
            try:
                Post.edit_post(form.cleaned_data, post_id)
                img_url = get_image_url_content(
                    form.cleaned_data.get('contents'))
                PostImage.add_use_post(img_url, post_id)
                pdf_url = get_pdf_url_content(
                    form.cleaned_data.get('contents'))
                PostPdf.add_use_post(pdf_url, post.post_id)

                transaction.savepoint_commit(sid)
            except:
                transaction.savepoint_rollback(sid)
                request.session['request_data'] = {
                    'post_status': 'Error',
                }
                request.session['form_data'] = form.cleaned_data
                return redirect(request.META.get('HTTP_REFERER', '/'))

        else:
            request.session['request_data'] = {
                'post_status': 'Error',
            }
            request.session['form_data'] = form.cleaned_data
            request.session['error_messages'] = get_error_message(request)

            return redirect(request.META.get('HTTP_REFERER', '/'))

        return redirect('/post')


class PostDelete(View):
    @staticmethod
    def post(request, post_id):
        post = Post.get_by_id(post_id)
        if post is None:
            raise Http404
        try:
            Post.delete_post(post_id)
        except:
            request.session['request_data'] = {
                'post_status': 'Error',
            }
            return redirect(request.META.get('HTTP_REFERER', '/'))

        return redirect('/post')


class PostStatus(View):
    @staticmethod
    def post(request, post_id):
        post = Post.get_by_id(post_id)
        if post is None:
            return JsonResponse({
                'status': 500, 'message': 'Not Change'}, status=500)

        form = PostStatusForm(request.POST)
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))
        if form.is_valid():
            sid = transaction.savepoint()
            try:
                Post.status_change(form.cleaned_data.get('status'), post_id)
                transaction.savepoint_commit(sid)

            except:
                transaction.savepoint_rollback(sid)
                return JsonResponse({
                    'status': 500, 'message': 'Not Delete'}, status=500)

        else:
            return JsonResponse({
                'status': 500, 'message': get_error_message(request)},
                status=500)

        return JsonResponse({
            'status': 200, 'message': 'Changed'},
            status=200)


class PostPreview(PostSetup):
    def get(self, request, post_id):
        post = Post.get_by_id(post_id)
        if post is None:
            raise Http404

        self.data.update({
            'title': 'プレビュー',
            'post': post,
        })
        return render(request, 'post_preview.html', {'data': self.data})


class Login(PostSetup):
    def get(self, request):
        self.data.update({
            'title': 'ログイン',
        })
        return render(request, 'login.html', {'data': self.data})

    @staticmethod
    def post(request):
        form = LoginForm(request.POST)
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/post')
            else:
                return redirect(request.META.get('HTTP_REFERER', '/'))

        else:
            request.session['request_data'] = {
                'login_status': 'Auth Error',
            }
            return redirect(request.META.get('HTTP_REFERER', '/'))


class Logout(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('/login')


class AppricationError(View):
    @staticmethod
    def get(request):
        data = {
            'title': 'Error',
            'noindex': True,
        }
        try:
            logger.error(sys.exc_info())
        except:
            pass
        return render(request, 'application_error.html',
                      {'data': data}, status=500)
