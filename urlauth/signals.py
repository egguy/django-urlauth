from django.dispatch import Signal

authkey_processed = Signal(providing_args=['key', 'request', 'user'])
