from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.sql.subqueries import DeleteQuery

from urlauth.models import AuthKey


def truncate_queryset(qs):
    """
    Deletes all records matched by queryset using

        DELETE from table WHERE <condition>

    query without fetching PK values for all items in original queryset
    unlike django's standard QuerySet.delete().

    See https://code.djangoproject.com/ticket/9519.
    """

    delete_query = qs.query.clone(DeleteQuery)

    # transaction management code is copied from QuerySet.update
    if not transaction.is_managed(using=qs.db):
        transaction.enter_transaction_management(using=qs.db)
        forced_managed = True
    else:
        forced_managed = False
    try:
        delete_query.get_compiler(qs.db).execute_sql(None)
        if forced_managed:
            transaction.commit(using=qs.db)
        else:
            transaction.commit_unless_managed(using=qs.db)
    finally:
        if forced_managed:
            transaction.leave_transaction_management(using=qs.db)


class Command(BaseCommand):
    help = "Remove expired keys from database"

    def handle(self, *args, **kwargs):
        qs = AuthKey.objects.filter(expired__lt=datetime.now())
        count = qs.count()

        # qs.delete() is grossly inefficient for larger querysets
        # and there can be a *LOT* of AuthKey's
        truncate_queryset(qs)

        print("%d keys deleted" % count)
