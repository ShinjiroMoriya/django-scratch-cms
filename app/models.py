import uuid
from django.db import models
from django.db.models.functions import Now
from datetime import datetime


class Post(models.Model):
    class Meta:
        db_table = 'post'
        ordering = ['-publish_date']

    post_id = models.CharField(max_length=255, editable=False,
                               default=uuid.uuid4)
    title = models.CharField(max_length=255)
    contents = models.TextField()
    status = models.CharField(default='draft', max_length=255)
    use_images = models.ManyToManyField('PostImage',
                                        related_name='post_image', blank=True)
    use_pdfs = models.ManyToManyField('PostPdf',
                                      related_name='post_pdf', blank=True)
    publish_date = models.DateTimeField(default=datetime.now)
    registration_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_published(cls):
        return cls.objects.filter(status='publish',
                                  publish_date__lte=Now())

    @classmethod
    def get_by_id(cls, post_id):
        return cls.objects.filter(post_id=post_id).first()

    @classmethod
    def create_post(cls, data):
        return cls.objects.create(
            title=data.get('title'),
            contents=data.get('contents'),
            publish_date=data.get('publish_date'),)

    @classmethod
    def edit_post(cls, data, post_id):
        cls.objects.filter(post_id=post_id).update(
            title=data.get('title'),
            contents=data.get('contents'),
            publish_date=data.get('publish_date'))

    @classmethod
    def status_change(cls, status, post_id):
        return cls.objects.filter(post_id=post_id).update(status=status)

    @classmethod
    def delete_post(cls, post_id):
        return cls.objects.filter(post_id=post_id).delete()


class PostImage(models.Model):
    class Meta:
        db_table = 'post_image'
        ordering = ['-registration_date']

    image_id = models.CharField(unique=True, max_length=255)
    image_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    registration_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.prefetch_related('post_image').all()

    @classmethod
    def get_by_image_url(cls, image_url):
        return cls.objects.filter(image_url=image_url).first()

    @classmethod
    def get_by_image_id(cls, image_id):
        return cls.objects.filter(image_id=image_id).first()

    @classmethod
    def add_use_post(cls, image_urls, post_id):
        post = Post.get_by_id(post_id)
        postimgs = []
        for iu in image_urls:
            postimgs.append(cls.objects.get(image_url=iu))
        post.use_images = postimgs

    @classmethod
    def create_image(cls, data):
        return cls.objects.create(
            image_id=data.get('image_id'),
            image_url=data.get('image_url'),
            title=data.get('title'),)

    @classmethod
    def delete_image(cls, image_id):
        return cls.objects.filter(image_id=image_id).delete()


class PostPdf(models.Model):
    class Meta:
        db_table = 'post_pdf'
        ordering = ['-registration_date']

    pdf_id = models.CharField(unique=True, max_length=255)
    pdf_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    registration_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    @classmethod
    def get_all(cls):
        return cls.objects.prefetch_related('post_pdf').all()

    @classmethod
    def get_by_pdf_url(cls, pdf_url):
        return cls.objects.filter(pdf_url=pdf_url).first()

    @classmethod
    def get_by_pdf_id(cls, pdf_id):
        return cls.objects.filter(pdf_id=pdf_id).first()

    @classmethod
    def add_use_post(cls, pdf_urls, post_id):
        post = Post.get_by_id(post_id)
        postpdfs = []
        for pu in pdf_urls:
            postpdfs.append(cls.objects.get(pdf_url=pu))
        post.use_pdfs = postpdfs

    @classmethod
    def create_pdf(cls, data):
        return cls.objects.create(
            pdf_id=data.get('pdf_id'),
            pdf_url=data.get('pdf_url'),
            title=data.get('title'))

    @classmethod
    def delete_pdf(cls, pdf_id):
        return cls.objects.filter(pdf_id=pdf_id).delete()
