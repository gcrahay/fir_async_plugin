from django.contrib.contenttypes.models import ContentType

from collections import OrderedDict

from incidents.models import BusinessLine

from fir_async.methods.jabber import XmppMethod
from methods.email import EmailMethod
from fir_async.tasks import handle_notification


class Notifications(object):
    def __init__(self):
        self.methods = OrderedDict()
        self.events = OrderedDict()

    def register_method(self, method, name=None, verbose_name=None):
        if not method.server_configured:
            return
        if name is not None:
            method.name = name
        if verbose_name is not None:
            method.verbose_name = verbose_name
        if not method.verbose_name:
            method.verbose_name = method.name
        self.methods[method.name] = method

    def register_event(self, name, signal, model, callback, verbose_name=None):
        if verbose_name is None:
            verbose_name = name
        self.events[name] = verbose_name

        signal.connect(callback, sender=model, dispatch_uid="fir_async.{}".format(name))

    def get_event_choices(self):
        return self.events.items()

    def get_method_choices(self):
        return [(obj.name, obj.verbose_name) for obj in self.methods.values()]


registry = Notifications()
registry.register_method(EmailMethod())
registry.register_method(XmppMethod())


def async_event(event, signal, model, verbose_name=None):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            instance, business_lines = func(*args, **kwargs)
            if instance is None:
                return instance, business_lines
            if isinstance(business_lines, BusinessLine):
                business_lines = [business_lines.path,]
            else:
                business_lines = list(business_lines.distinct().values_list('path', flat=True))
            handle_notification.delay(ContentType.objects.get_for_model(instance).pk,
                                      instance.pk,
                                       business_lines,
                                      event)
            return instance, business_lines

        registry.register_event(event, signal, model, wrapper_func, verbose_name)
        return wrapper_func
    return decorator_func
