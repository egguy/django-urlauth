from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from urlauth.models import AuthKey


class Command(BaseCommand):
    help = "Remove expired keys from database"

    def handle(self, *args, **kwargs):
        qs = AuthKey.objects.filter(expired__lt=datetime.now())
        count = qs.count()

        # qs.delete() is grossly inefficient for larger querysets
        # and there can be a *LOT* of AuthKey's
        with transaction.atomic():
            qs._raw_delete(qs.db)

        print("%d keys deleted" % count)
