import os
import tempfile
from django.conf import settings
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cloudinary.api import delete_resources
from api.logger import logger


__all__ = ['delete_resources']


def file_ext_check(ext: str) -> bool:
    ext = ext.lower()
    for i in ['.jpg', '.jpeg', '.png', '.gif']:
        if ext == i:
            return True

    return False


def file_uploader(file: any) -> dict:
    temp = tempfile.NamedTemporaryFile()
    results = {}

    try:
        write_data = file.read()

        temp.write(write_data)
        temp.seek(0)

        if int(settings.MAX_UPLOAD_SIZE) > len(write_data):
            results = upload(temp.name)

        temp.close()

    except Exception as ex:
        logger.info(ex)
        pass

    finally:
        temp.close()

    return results


def get_image_url(public_id: str, sizes=None) -> [dict, dict] or [None, None]:
    try:
        if sizes is None:
            sizes = {}
        return cloudinary_url(
            public_id,
            format="jpg",
            width=sizes.get('width'),
            height=sizes.get('height'),
            crop='fill',
            radius=sizes.get('radius'),
            secure=True)

    except:
        return None, None


def get_pdf_url(public_id: str) -> [dict, dict] or [None, None]:
    try:
        return cloudinary_url(
            public_id,
            format="pdf",
            secure=True)

    except:
        return None, None


def set_image_upload(file, sizes=None):

    _, ext = os.path.splitext(file.name)

    if file_ext_check(ext) is False:
        return 500, {'message': 'Ext'}

    upload_result = file_uploader(file)

    if upload_result == {}:
        return 500, {'message': 'NotRegisterFile: image_data_limit_over'}

    try:
        images_url, options = get_image_url(
            upload_result['public_id'], sizes)

        if images_url is None:
            return 500, {'message': 'NotRegisterFile: images_url'}

        return 200, {
            'title': file.name,
            'image_id': upload_result['public_id'],
            'image_url': images_url
        }

    except:
        return 500, {'message': 'NotRegisterFile: except'}


def set_pdf_upload(file):

    _, ext = os.path.splitext(file.name)

    if ext.lower() != '.pdf':
        return 500, {'message': 'Ext'}

    upload_result = file_uploader(file)

    if upload_result == {}:
        return 500, {'message': 'NotRegisterFile: image_data_limit_over'}

    try:
        pdf_url, options = get_pdf_url(
            upload_result['public_id'])

        if pdf_url is None:
            return 500, {'message': 'NotRegisterFile: images_url'}

        return 200, {
            'title': file.name,
            'pdf_id': upload_result['public_id'],
            'pdf_url': pdf_url,
        }

    except:
        return 500, {'message': 'NotRegisterFile: except'}
