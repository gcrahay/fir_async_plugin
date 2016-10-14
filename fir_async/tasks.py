from __future__ import absolute_import

from celery import shared_task
from django.db import models

from django.contrib.auth.models import User, Permission
from incidents.models import BusinessLine

_perm_id = None


def get_perm_id():
    global _perm_id
    if _perm_id is not None:
        return _perm_id
    perm_obj = Permission.objects.get(content_type__app_label='incidents',
                                      codename='view_incidents')
    _perm_id = perm_obj.pk
    return _perm_id


def get_templates(event, business_line=None):
    from fir_async.models import NotificationTemplate
    templates = list(NotificationTemplate.objects.filter(event=event, business_lines=business_line).order_by('id'))
    return templates


def get_user_templates(event, business_lines):
    global_users = User.objects.filter(
        models.Q(groups__permissions=get_perm_id()) | models.Q(user_permissions=get_perm_id()) | models.Q(
            is_superuser=True)).distinct()
    global_templates = get_templates(event)
    # User with global permission => global templates first
    users = {user: list(global_templates) for user in global_users}
    business_lines = {bl: bl.get_ancestors() for bl in BusinessLine.objects.filter(path__in=business_lines).order_by('depth')}
    depth = 1
    all_templates = {}
    while len(business_lines):
        for lower in business_lines.keys():
            if lower not in all_templates:
                all_templates[lower] = []
            path = business_lines[lower]
            if len(path) > depth:
                current_bl = path[depth-1]
                templates = get_templates(event, current_bl)
            else:
                templates = get_templates(event, lower)
                business_lines.pop(lower, None)
                current_bl = lower
            if len(templates):
                users_done = []
                # User with global permission => top-down
                for user in global_users:
                    users[user].extend(templates)
                    users_done.append(user)
                role_users = User.objects.filter(accesscontrolentry__business_line=current_bl).filter(
                                                 accesscontrolentry__role__permissions=get_perm_id()).distinct()
                # User with bl role => this bl templates first
                for user in role_users:
                    users_done.append(user)
                    if user not in users:
                        users[user] = list(templates).extend(all_templates[lower])
                    else:
                        users[user] = list(templates).extend(users[user])
                # Other users => append the templates
                for user in users:
                    if user not in users_done:
                        users[user].extend(templates)
                all_templates[lower].extend(templates)
            else:
                role_users = User.objects.filter(accesscontrolentry__business_line=current_bl).filter(
                                                 accesscontrolentry__role__permissions=get_perm_id()).distinct()
                for user in role_users:
                    if user not in users:
                        users[user] = list(all_templates[lower])
        depth += 1
    # User without global permission => global templates last
    for user in users:
        if user not in global_users:
            users[user].extend(global_templates)
    return users


@shared_task
def handle_notification(content_type, instance, business_lines, event):
    from fir_async.registry import registry
    from django.contrib.contenttypes.models import ContentType
    try:
        model = ContentType.objects.get_for_id(content_type).model_class()
    except ContentType.DoesNotExist:
        print "Unknown content type"
        return
    try:
        instance = model.objects.get(id=instance)
    except model.DoesNotExist:
        print "Unknown instance"
        return
    users = get_user_templates(event, business_lines)
    for method in registry.methods.values():
        method.send(event, users, instance, business_lines)
