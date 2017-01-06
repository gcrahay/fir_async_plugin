from django import template
from django.utils.translation import ugettext_lazy as _

from fir_async.registry import registry

register = template.Library()


@register.inclusion_tag('fir_async/actions.html')
def notification_actions():
    actions = {}
    for method_name, method_object in registry.methods.items():
        if len(method_object.options):
            actions[method_name] = method_object.verbose_name
    return {'actions': actions}


@register.inclusion_tag('fir_async/actions_form.html', takes_context=True)
def notification_forms(context):
    actions = {}
    for method_name, method_object in registry.methods.items():
        if len(method_object.options):
            actions[method_name] = method_object.form(user=context[ 'user'])
    return {'actions': actions}
