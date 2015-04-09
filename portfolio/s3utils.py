from storages.backends.s3boto import S3BotoStorage

from django.conf import settings

StaticS3BotoStorage = lambda: S3BotoStorage(
    location=settings.STATIC_DIR,
    secure_urls=False,
    default_acl='public-read-write',
)

MediaS3BotoStorage = lambda: S3BotoStorage(
    location=settings.MEDIA_DIR,
    secure_urls=False,
    default_acl='public-read-write',
)